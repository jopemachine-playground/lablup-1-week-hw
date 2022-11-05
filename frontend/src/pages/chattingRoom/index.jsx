import React, { useState, useEffect, useRef } from "react";
import styled from "styled-components";
import axios from "axios";
import { io } from "socket.io-client";
import API from '../../api';

export default function ChattingRoom(props) {
  const [chat, setChat] = useState("");
  const [chatlogs, setChatlogs] = useState([]);
  const chatlogsRef = useRef(chatlogs);
  const chatEventHandler = useRef();
  const chattingLogArea = useRef();

  useEffect(() => {
    chatlogsRef.current = chatlogs;
  });

  useEffect(() => {
    chatEventHandler.current = (message) => {
      setChatlogs([...chatlogsRef.current, message]);
    };

    const socket = io(
      `${API.chatting_backend}/ws-chatting`,
      {
        transports: ["websocket"],
        path: "/socket.io",
        port: 3000,
        forceNew: true,
      }
    );

    axios
      .get(`${API.chatting_backend}/api/v1/chattingRoom/chats`)
      .then(({ data }) => {
        console.log("data", data);
        setChatlogs(data);
      });

    socket.on("chat", (msg) => {
      console.log("chat", msg);
      chatEventHandler.current(msg);
    });
  }, []);

  useEffect(() => {
    chattingLogArea.current.scrollTop = chattingLogArea.current.scrollHeight;
  }, [chatlogs])

  const chatBtnClickHandler = () => {
    axios
      .put(`${API.chatting_backend}/api/v1/chattingRoom/chat`, {
        chat,
      })
      .then(({ data }) => {
        setChat("");
        if (data !== true) console.error(data);
      });
  };

  const renderTextArea = () => {
    return (
      <ChatLogArea ref={chattingLogArea}>
        {chatlogs.map((chatlog, idx) => {
          const speaker =
            props.userId === chatlog.userId ? (
              <MyChat>{chatlog.userId}: </MyChat>
            ) : (
              <OthersChat>{chatlog.userId}: </OthersChat>
            );

          return (
            <div key={`log-${idx}`}>
              {speaker}
              <div>{chatlog.msg}</div>
            </div>
          );
        })}
      </ChatLogArea>
    );
  };

  return (
    <OuterContainer>
      <Title>채팅방</Title>
      <SubTitle>채팅 로그</SubTitle>
      {renderTextArea()}
      <ChatInputArea
        placeholder={"텍스트를 입력하세요."}
        value={chat}
        onChange={(e) => setChat(e.target.value)}
      />
      <ChatButton
        className={"btn btn-primary btn-block"}
        onClick={chatBtnClickHandler}
      >
        Send
      </ChatButton>
    </OuterContainer>
  );
}

const Title = styled.div`
  font-size: 25px;
  margin-bottom: 20px;
`;

const SubTitle = styled.div`
  font-size: 15px;
  margin-bottom: 10px;
`;

const OuterContainer = styled.span`
  margin-left: 60px;
  margin-top: 30px;
  height: 80%;
  width: 80%;
  display: flex;
  flex-direction: column;
`;

const ChatButton = styled.button`
  width: 100px;
  height: 45px;
  margin-bottom: 30px;
`;

const ChatInputArea = styled.textarea`
  width: 80%;
  height: 10%;
  margin-bottom: 20px;
`;

const ChatLogArea = styled.div`
  overflow-y: scroll;
  height: 60%;
  margin-bottom: 15px;
`;

const MyChat = styled.div`
  display: inline-block;
  color: #fc8dea;
`;

const OthersChat = styled.div`
  display: inline-block;
  color: #ffe291;
`;
