use std::sync::{Arc, Condvar, Mutex};

pub struct MessageSender<'a, Message> {
    v: &'a mut Vec<Message>,
    max: usize,
}

impl<'a, Message> MessageSender<'a, Message> {
    pub fn send(&mut self, m: Message) {
        self.v.push(m);
    }

    pub fn get_max(&self) -> usize {
        self.max
    }
}

#[derive(Default)]
#[cfg(feature = "log")]
struct Logs {
    states_processed: u32,
    used_channel: u32,
    put_into_channel: u32,
    woke_up: u32,
    waited: u128,
}

#[cfg(feature = "log")]
impl std::fmt::Display for Logs {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "Thread processed {} states, ", self.states_processed)?;
        write!(f, "took from the channel {} times, ", self.used_channel)?;
        write!(f, "put into the channel {} times, ", self.put_into_channel)?;
        write!(f, "woke up {} times, ", self.woke_up)?;
        write!(f, "and waited {} ms in total.", self.waited / 1_000_000)?;
        Ok(())
    }
}

struct MT<MessageType> {
    waiting: u8,
    max: usize,
    messages: Vec<MessageType>,
}

pub struct RunParameters {
    pub take: u32,
    pub put_after: usize,
    pub leave: usize,
    pub num_threads: u8,
}

//add more parameters?
pub fn run<Message, Parameters>(
    rp: RunParameters,
    p: &Parameters,
    initial: Message,
    process: fn(&Parameters, MessageSender<'_, Message>, Message) -> usize,
) -> usize
where
    Message: Sync + Send,
    Parameters: Sync + Send,
{
    let arc = Arc::new((
        Mutex::new(MT {
            waiting: 0,
            max: 0,
            messages: vec![initial],
        }),
        Condvar::new(),
    ));
    std::thread::scope(|s| {
        for _ in 0..rp.num_threads {
            s.spawn(|| {
                #[cfg(feature = "log")]
                let mut logs = Logs::default();

                let mut my_states = Vec::<Message>::new();
                let mut my_max = 0;
                let pair = Arc::clone(&arc);

                loop {
                    #[cfg(feature = "log")]
                    {
                        logs.used_channel += 1;
                    }

                    {
                        #[cfg(feature = "log")]
                        let started = std::time::SystemTime::now();

                        let (lock, cv) = &*pair;
                        let mut mutex = lock.lock().unwrap();
                        mutex.waiting += 1;
                        while (*mutex.messages).is_empty() {
                            if mutex.waiting == rp.num_threads {
                                #[cfg(feature = "log")]
                                {
                                    logs.waited += std::time::SystemTime::now()
                                        .duration_since(started)
                                        .unwrap()
                                        .as_nanos();
                                    println!("{logs}");
                                }
                                {
                                    mutex.max = std::cmp::max(my_max, mutex.max);
                                }
                                cv.notify_all();
                                return;
                            }
                            mutex = cv.wait(mutex).unwrap();
                            #[cfg(feature = "log")]
                            {
                                logs.woke_up += 1;
                            }
                        }
                        #[cfg(feature = "log")]
                        {
                            logs.waited += std::time::SystemTime::now()
                                .duration_since(started)
                                .unwrap()
                                .as_nanos();
                        }
                        mutex.waiting -= 1;
                        for _ in 0..rp.take {
                            if let Some(m) = mutex.messages.pop() {
                                my_states.push(m);
                            } else {
                                break;
                            }
                        }
                    }

                    while let Some(m) = my_states.pop() {
                        #[cfg(feature = "log")]
                        {
                            logs.states_processed += 1;
                        }
                        my_max = std::cmp::max(
                            my_max,
                            (process)(
                                p,
                                MessageSender {
                                    v: &mut my_states,
                                    max: my_max,
                                },
                                m,
                            ),
                        );
                        if my_states.len() > rp.put_after {
                            #[cfg(feature = "log")]
                            {
                                logs.put_into_channel += 1;
                            }
                            let (lock, cv) = &*pair;
                            let mut mutex = lock.lock().unwrap();
                            mutex.messages.append(&mut my_states.split_off(rp.leave));
                            cv.notify_all();
                        }
                    }
                }
            });
        }
    });

    let (lock, _cv) = &*arc;
    let l = lock.lock().unwrap();
    l.max
}
