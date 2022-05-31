import React, { useEffect } from "react";
import styled from "styled-components";
import { useState } from "react";
import socketIoClient from 'socket.io-client';
import './main.css';

const socketServer = 'http://192.168.0.9:5555'; //서버 주소

const socket = socketIoClient.connect(socketServer);

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
    const [image, setImage] = useState(['','']);
    useEffect(() => {
        socket.on('connection' , sock => {
            console.log('connected');
        });
    }, []);

    useEffect(() => {
        socket.on('processResult', (data) => {
            setImage(Buffer.from(data, "base64").toString());
        })
    })

    return (<PageBody >
        <div className="title">마스크 미착용자 알림 프로그램</div>
        <div className="type">{image[0]}</div>
        <ImageBox>{ image[1] !== '' &&<img src={"data:image/jpeg;base64," + image[1]} />}</ImageBox>
    </PageBody>
    )
}

export default MainPage;