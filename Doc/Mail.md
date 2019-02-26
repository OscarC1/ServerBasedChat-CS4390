**From:** Zhou, Shuang 
 **Sent:** Thursday, February 21, 2019 12:26 PM
 **To:** 'mailto:gio@utdallas.edu' <<mailto:gio@utdallas.edu>>
 **Subject:** RE: Server based chat questions

 

Hi,

 

For the question “The client cannot simultaneously listen for messages and send messages from the same TCP socket”, I think the better way to solve it is to use “InputStream” to read and “OutputStream to write. I hope this can solve your question.

 

Regards,

 

Shuang

 

**From:** Le, Khiem 
 **Sent:** Thursday, February 21, 2019 12:07 PM
 **To:** Giovanetti, Seth Thomas <[gio@utdallas.edu](mailto:gio@utdallas.edu)>
 **Cc:** Zhou, Shuang <[sxz170012@utdallas.edu](mailto:sxz170012@utdallas.edu)>
 **Subject:** RE: Server based chat questions

 

Seth,

 

I am going to answer your questions related to the concept of sockets. As for the questions related to the implementation details, I have forwarded your mail to our TA, who will answer them. It is preferable that the TA answers these questions to ensure consistency, since she will be reviewing and grading your code. However, if there are unresolved issues, let me know, I would be glad to help.

 

I haven’t gone into the details of TCP in class yet, but a TCP socket corresponds to a TCP connection, and a TCP connection is bidirectional. So with one TCP socket you can send and receive data. As for how to juggle the sending and receiving processes, there is a variety of ways. You do not need to send and receive at exactly the same time, and socket operations can be made non-blocking. Our TA can elaborate on that.

I believe you have an error when sending to the listening socket because it is the welcoming socket from the lectures. It is by nature listening only. You should use a connection socket to send/receive data.

At the server side, for a given application, all the TCP sockets for different clients have the same port #. They are differentiated because in TCP, a socket is identified by a 4-tuple.

Hope this helps,

Dr. Le

 

 

**From:** Giovanetti, Seth Thomas <[gio@utdallas.edu](mailto:gio@utdallas.edu)> 
 **Sent:** Wednesday, February 20, 2019 2:27 PM
 **To:** Le, Khiem <[kvl140030@utdallas.edu](mailto:kvl140030@utdallas.edu)>
 **Subject:** Server based chat questions

I have a number of questions about the server-based chat project.

During authentication, the client knows the specific order of requests to listen for, and can alternate on the same port. The server is reactive, and can quickly send a message out via the listening UDP socket and return to listening.

Once TCP is established, there's a problem. The client cannot simultaneously listen for messages and send messages from the same TCP socket. Windows will NOT allow me to send a message from a dedicated listening socket (WinError 10022, invalid argument), and a "connected" socket cannot passively listen for messages; receiving TCP messages is blocking.

The paradigm, as best as I've been able to understand it, is this: The client needs a dedicated socket (and a dedicated thread) for listening for messages, and a second dedicated socket for sending TCP messages. Likewise, the server needs a dedicated socket for listening, and a second dedicated socket for sending. 

Is this correct? I feel like parts of this must be wrong, but I'm not sure what. 

Further, does the server need a dedicated TCP port for each new client?

Any help is appreciated.

Thanks,

Seth Giovanetti