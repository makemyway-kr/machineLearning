import React, { useEffect } from "react";
import styled from "styled-components";
import { useState } from "react";
import socketIoClient from 'socket.io-client';
import './main.css';

const socketServer = ''; //서버 주소

const PageBody = styled.div`
    width : 100%;
    justify-content : center;
    text-align : center;
`

const ImageBox = styled.div`
    width : 80%;
    height : 60%;
    object-fit : cover;    
`

const MainPage = () => {
    const [image, setImage] = useState('');
    const [socket, setSocket] = useState(socketIoClient(socketServer));
    useEffect(() => {
        window.onload(e => {
            socket.on('connection', sock => {
                sock.join('video connection');
            })
        })
    }, []);

    useEffect(() => {
        socket.join('video connection');
        socket.on('processResult', (data) => {
            setImage(Buffer.from(data, "base64").toString());
        })
    })

    return (<PageBody >
        <div className="title">마스크 미착용자 알림 프로그램</div>
        <ImageBox><img src={"data:image/jpeg;base64," + image} /></ImageBox>
    </PageBody>
    )
}

export default MainPage;