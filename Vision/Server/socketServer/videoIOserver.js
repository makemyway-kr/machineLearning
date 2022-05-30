import { Server } from 'socket.io'
import http from 'http';
//비디오 중계용 js서버
const server = http.createServer().listen(6666);

var io = new Server(server)

//비디오를 받아서 서버에 넘겨줌.
io.sockets.on('connection', (socket) => {
    socket.join('video connection');
    socket.on('videoIncoming', (videoData) => {
        console.log('video incoming');
        io.sockets.in('video connection').emit('videoProcess', videoData);
    });

    socket.on('processResult', (resultData) => {
        io.sockets.in('video conneciton').emit('result', resultData);
    })
});