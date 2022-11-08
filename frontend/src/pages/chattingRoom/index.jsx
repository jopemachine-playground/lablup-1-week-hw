import React, {useState, useEffect, useRef, useMemo} from 'react';
import styled from 'styled-components';
import axios from 'axios';
import {io} from 'socket.io-client';
import API from '../../api.js';
import {parseCookie} from '../../utils.js';

export default function ChattingRoom(props) {
	const [chat, setChat] = useState('');
	const [chatlogs, setChatlogs] = useState([]);
	const chatlogsRef = useRef(chatlogs);
	const chatEventHandler = useRef();
	const chattingLogArea = useRef();
	const [ws, setWs] = useState();
	const userId = useMemo(() => parseCookie(document.cookie)['user_id'], []);

	useEffect(() => {
		chatlogsRef.current = chatlogs;
	});

	useEffect(() => {
		chatEventHandler.current = message => {
			setChatlogs([...chatlogsRef.current, message]);
		};
	}, []);

	useEffect(() => {
		axios
			.get(`${API.CHATTING_BACKEND}/api/v1/ping`, {
				withCredentials: true,
			})
			.catch(error => {
				if (error.response && error.response.status === 401) {
					props.setPage('SignIn');
					return;
				}

				alert(error);
			});
	}, []);

	useEffect(() => {
		const socket = io(
			'localhost:8080/ws-chatting',
			{
				transports: ['websocket', 'polling', 'flashsocket'],
				path: '/socket.io',
				port: 8080,
				forceNew: true,
			},
		);

		socket.on('connect', () => {
			console.log('ws for chatting connected successfully.');
		});

		socket.on('message', message => {
			chatEventHandler.current(JSON.parse(message));
		});

		setWs(socket);
	}, []);

	useEffect(() => {
		chattingLogArea.current.scrollTop = chattingLogArea.current.scrollHeight;
	}, [chatlogs]);

	const handleChatBtnClick = () => {
		if (ws) {
			const chatData = JSON.stringify({
				message: chat,
				created_by: userId,
				created_at: new Date().toLocaleString(),
			});

			ws.emit('message', chatData);
			setChat('');
		}
	};

	const handleLogout = () => {
		axios.get(`${API.CHATTING_BACKEND}/api/v1/signout`, {
			withCredentials: true,
		}).then(() => {
			props.setPage('SignIn');
		}).catch(() => {
			alert('로그아웃에 실패했습니다!');
		});
	};

	const renderTextArea = () => (
		<ChatLogArea ref={chattingLogArea}>
			{chatlogs.map((chatlog, idx) => {
				const speaker = userId === chatlog.created_by ? (
					<MyChat>{chatlog.created_by}: </MyChat>
				) : (
					<OthersChat>{chatlog.created_by}: </OthersChat>
				);

				return (
					<div key={`log-${idx}`} style={{
						display: 'flex',
						flexDirection: 'row',
					}}>
						<CreatedAt>{`[${chatlog.created_at}]`}</CreatedAt>
						{speaker}
						<div>{chatlog.message}</div>
					</div>
				);
			})}
		</ChatLogArea>
	);

	return (
		<OuterContainer>
			<Title>채팅방</Title>
			<SubTitle>채팅 로그</SubTitle>
			{renderTextArea()}
			<ChatInputArea
				placeholder={'텍스트를 입력하세요.'}
				value={chat}
				onChange={e => setChat(e.target.value)}
			/>
			<div style={{
				display: 'flex',
				flexDirection: 'row',
			}}>
				<ChatButton
					className={'btn btn-primary btn-block'}
					onClick={handleChatBtnClick}
				>
					보내기
				</ChatButton>

				<LogoutButton
					className={'btn btn-primary btn-block'}
					onClick={handleLogout}
				>
					로그아웃
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

const CreatedAt = styled.div`
	display: inline-block;
	color: #777;
	margin-right: 3px;
`;

const MyChat = styled.div`
	display: inline-block;
	color: #fc8dea;
	margin-right: 3px;
`;

const OthersChat = styled.div`
	display: inline-block;
	color: #ffe291;
	margin-right: 3px;
`;
