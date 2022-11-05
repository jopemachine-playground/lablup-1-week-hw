import React, { useState } from "react";
import axios from "axios";
import { FormText, Input, Button } from "reactstrap";
import API from '../../api';

const getErrorMsg = (errCode) => {
  switch (errCode) {
    case 400:
      return "잘못된 요청입니다.";
    case 420:
      return "잘못된 아이디나 패스워드입니다.";
    default:
      return "잠시 후 다시 시도해주시기 바랍니다.";
  }
};

const SignInPage  = (props) => {
  const [userId, setUserId] = useState("");
  const [userPW, setUserPW] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const handleSignIn = () => {
    if (userId && userPW) {
      axios
        .post(`${API.chatting_backend}/api/v1/signin`, {
          id: userId,
          pw: userPW
        })
        .then(({ data: sessionId }) => {
          console.log('logged in user\'s session id', sessionId);

          window.sessionStorage.setItem('user-id', userId);
          window.sessionStorage.setItem('session-id', sessionId);
          window.location.href = "/";
        })
        .catch((err) => {
          setErrorMsg({ errorMsg: getErrorMsg(err.response.status) });
        });
    }
  };

  return (
    <div style={{}}>
      <Input onChange={e => setUserId(e.target.value)} value={userId} placeholder="아이디" />
      <Input
        type="password"
        onChange={e => setUserPW(e.target.value)}
        value={userPW}
        placeholder="비밀번호"
      />

      {errorMsg && <FormText>{errorMsg}</FormText>}

      <Button
        color="primary"
        onClick={handleSignIn}
      >
        로그인
      </Button>

      <Button
        color="primary"
        onClick={() => props.setPage("SignUp")}
      >
        회원가입
      </Button>
    </div>
  )
}

export default SignInPage;
