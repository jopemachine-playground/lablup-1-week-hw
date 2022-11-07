import React, {useState} from 'react';
import axios from 'axios';
import {FormText, Input, Button} from 'reactstrap';
import API from '../../api.js';

const getErrorMessage = errorCode => {
	switch (errorCode) {
		case 400:
			return '잘못된 요청입니다.';
		case 419:
			return '이미 존재하는 아이디입니다.';
		default:
			return '잠시 후 다시 시도해주시기 바랍니다.';
	}
};

const SignupPage = props => {
	const [userId, setUserId] = useState('');
	const [userPW, setUserPW] = useState('');
	const [userPWConf, setUserPWConf] = useState('');
	const [errorMessage, setErrorMessage] = useState('');

	const handleSignUp = () => {
		if (!userId || !userPW || !userPWConf) {
			return;
		}

		if (userPW === userPWConf) {
			axios
				.post(`${API.chatting_backend}/api/v1/signup`, {
					id: userId,
					pw: userPW,
				})
				.then(({data}) => {
					props.setPage('SignIn');
				})
				.catch(error => {
					setErrorMessage(getErrorMessage(error.response.status));
				});
		} else {
			setErrorMessage('비밀번호와 비밀번호 확인이 같지 않습니다.');
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
				placeholder='비밀번호'
				value={userPW}
				style={{
					marginBottom: 3,
				}}
			/>
			<Input
				type='password'
				onChange={e => setUserPWConf(e.target.value)}
				placeholder='비밀번호 확인'
				value={userPWConf}
				style={{
					marginBottom: 8,
				}}
			/>

			{errorMessage && <FormText>{errorMessage}</FormText>}
			<Button
				color='primary'
				onClick={() => props.setPage('SignIn')}
				style={{
					marginBottom: 3,
				}}
			>
        로그인
			</Button>

			<Button
				color='primary'
				onClick={handleSignUp}
				style={{}}
			>
        회원가입
			</Button>
		</div>
	);
};

export default SignupPage;
