import socketio from 'socketio';
import http from 'http';
//비디오 중계용 js서버
const server = http.createServer().listen(6666);

var io = socketio.listen(server);

//비디오를 받아서 서버에 넘겨줌.
io.sockets.on('connection', (socket) => {
    socket.join('video connection');
    socket.on('videoIncoming', (videoData) => {
        io.sockets.in('video connection').emit('videoProcess', videoData);
    });

    socket.on('processResult', (resultData) => {
        io.sockets.in('video conneciton').emit('result', resultData);
    })
});