import React, {useState} from 'react';
import axios from 'axios';
import {FormText, Input, Button} from 'reactstrap';
import API from '../../api.js';

const getErrorMessage = errorCode => {
	switch (errorCode) {
		case 400:
			return '잘못된 요청입니다.';
		case 401:
			return '잘못된 아이디나 패스워드입니다.';
		case 500:
			return '서버에서 문제가 발생했습니다.';
		default:
			return '잠시 후 다시 시도해주시기 바랍니다.';
	}
};

const SignInPage = props => {
	const [userId, setUserId] = useState('');
	const [userPW, setUserPW] = useState('');
	const [errorMessage, setErrorMessage] = useState('');

	const handleSignIn = () => {
		if (userId && userPW) {
			axios
				.post(`${API.CHATTING_BACKEND}/api/v1/signin`, {
					id: userId,
					pw: userPW,
				}, {
					withCredentials: true,
				})
				.then(({data: sessionId}) => {
					console.log('logged in user\'s session id', sessionId);
					props.setPage('ChattingRoom');
				})
				.catch(error => {
					setErrorMessage(getErrorMessage(error.response.status));
				});
		}
	};

	return (
		<div style={{
			marginTop: 12,
			marginLeft: 12,
			display: 'flex',
			flexDirection: 'column',
		}}>
			<Input onChange={e => setUserId(e.target.value)} value={userId} placeholder='아이디' style={{
				marginBottom: 3,
			}}/>
			<Input
				type='password'
				onChange={e => setUserPW(e.target.value)}
				value={userPW}
				placeholder='비밀번호'
				style={{
					marginBottom: 12,
				}}
			/>

			{errorMessage && <FormText>{errorMessage}</FormText>}

			<Button
				color='primary'
				onClick={handleSignIn}
				style={{
					marginBottom: 3,
				}}
			>
				로그인
			</Button>

			<Button
				color='primary'
				onClick={() => props.setPage('SignUp')}
			>
				회원가입
			</Button>
		</div>
	);
};

export default SignInPage;
