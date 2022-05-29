import React, { useEffect } from "react";
import styled from "styled-components";
import { useState } from "react";
import socketIoClient from 'socket.io-client';
const socketServer = '';
const imageBox = styled.div`
    width : 80%;
    height : 60%;
    object-fit : cover;    
`

const MainPage = () => {
    const [image, setImage] = useState('');
    const [socket,setSocket] = useState(socketIoClient(socketServer));
    useEffect(() => {
        window.onload(e => {
            socket.on('connection' , sock => {
                sock.join('video connection');
            })
        })
    },[]);

    useEffect(() => {
        socket.join('video connection');
        socket.on('processResult' , (data) => {
            setImage(data);
        })
    })
}

export default MainPage;