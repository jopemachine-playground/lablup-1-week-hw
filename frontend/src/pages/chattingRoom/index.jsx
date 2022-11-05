import React, { useState, useEffect, useRef } from "react";
import styled from "styled-components";
import axios from "axios";
import { io } from "socket.io-client";
import API from '../../api';

const userId = window.localStorage.getItem('user-id');
const sessionId = window.localStorage.getItem('session-id');

export default function ChattingRoom(props) {
  const [chat, setChat] = useState("");
  const [chatlogs, setChatlogs] = useState([]);
  const chatlogsRef = useRef(chatlogs);
  const chatEventHandler = useRef();
  const chattingLogArea = useRef();
  const [ws, setWs] = useState();

  useEffect(() => {
    chatlogsRef.current = chatlogs;
  });

  useEffect(() => {
    chatEventHandler.current = (message) => {
      setChatlogs([...chatlogsRef.current, message]);
    };
  }, []);

  useEffect(() => {
    axios
    .post(`${API.chatting_backend}/api/v1/chattingRoom/chats`, {
      id: userId,
      'session-id': sessionId,
    })
    .then(({ data }) => {
      console.log("data", data);
      setChatlogs(data.chats);
    })
    .catch(e => {
      alert(e)
    });
  }, []);

  useEffect(() => {
    const socket = io(
      `${API.chatting_backend}/ws-chatting`,
      {
        // transports: ["websocket"],
        port: 8080,
        // forceNew: true,
      }
    );

    socket.on("connect", () => {
      console.log("ws for chatting connected successfully.");
    });

    socket.on("chat", (msg) => {
      console.log("chat", msg);
      chatEventHandler.current(msg);
    });

    setWs(socket);
  }, []);

  useEffect(() => {
    chattingLogArea.current.scrollTop = chattingLogArea.current.scrollHeight;
  }, [chatlogs])

  const handleChatBtnClick = () => {
    if (ws) {
      ws.emit('chat', chat)
    }

    // axios
    //   .put(`${API.chatting_backend}/api/v1/chattingRoom/chat`, {
    //     chat,
    //   })
    //   .then(({ data }) => {
    //     setChat("");
    //     if (data !== true) console.error(data);
    //   });
  };

  const handleLogout = () => {
    axios.get(`${API.chatting_backend}/api/v1/signout`).then(() => {
      props.setPage("SignIn");
    }).catch(() => {
      alert("Failed to logout");
    })
  }

  const renderTextArea = () => {
    return (
      <ChatLogArea ref={chattingLogArea}>
        {chatlogs.map((chatlog, idx) => {
          const speaker = userId === chatlog.created_by ? (
              <MyChat>{chatlog.created_by}: </MyChat>
            ) : (
              <OthersChat>{chatlog.created_by}: </OthersChat>
            );

          return (
            <div key={`log-${idx}`}>
              {speaker}
              <div>{`[${chatlog.created_at}] ${chatlog.message}`}</div>
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
      <div style={{
        display: 'flex',
        flexDirection: 'row'
      }}>
        <ChatButton
          className={"btn btn-primary btn-block"}
          onClick={handleChatBtnClick}
        >
          Send
        </ChatButton>

        <LogoutButton
          className={"btn btn-primary btn-block"}
          onClick={handleLogout}
        >
          Logout
        </LogoutButton>
      </div>
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
  height: 25px;
  margin-bottom: 30px;
`;

const LogoutButton = styled.button`
  width: 100px;
  height: 25px;
  margin-bottom: 30px;
  margin-left: 6px;
`;

const ChatInputArea = styled.textarea`
  width: 400px;
  height: 30px;
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
