import { Server } from 'socket.io'
import http from 'http';
//비디오 중계용 js서버
const server = http.createServer().listen(5555);

var io = new Server(server)

//비디오를 받아서 서버에 넘겨줌.
io.sockets.on('connection', (socket) => {
    socket.join('video connection');
    socket.on('videoIncoming', (videoData) => {
        console.log('video incoming');
        io.emit('videoProcess', videoData);
    });

    socket.on('noMask', (resultData) => {
        console.log(resultData);
        io.sockets.emit('result', ['noMask' ,resultData]);
    })

    socket.on('partialMask',(resultData) =>{
        console.log(resultData);
        io.sockets.emit('result', ['partialMask' , resultData])
    })
});