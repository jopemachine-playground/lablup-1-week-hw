import React, { useState } from "react";
import axios from "axios";
import { FormText, Input, Button } from "reactstrap";
import API from '../../api';

const getErrorMsg = (errCode) => {
  switch (errCode) {
    case 400:
      return "잘못된 요청입니다.";
    case 419:
      return "이미 존재하는 아이디입니다.";
    default:
      return "잠시 후 다시 시도해주시기 바랍니다.";
  }
};

const SignupPage = (props) => {
  const [userId, setUserId] = useState("");
  const [userPW, setUserPW] = useState("");
  const [userPWConf, setUserPWConf] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const handleSignUp = () => {
    if (!userId || !userPW || !userPWConf) return;

    if (userPW === userPWConf) {
      axios
        .post(`${API.chatting_backend}/api/v1/signup`, {
          id: userId,
          pw: userPW,
        })
        .then(({ data }) => {
          props.setPage('SignIn');
        })
        .catch((err) => {
          setErrorMsg(getErrorMsg(err.response.status));
        });
    } else {
      setErrorMsg("비밀번호와 비밀번호 확인이 같지 않습니다.");
    }
  };

  return (
    <div style={{}}>
      <Input onChange={e => setUserId(e.target.value)} value={userId} placeholder="아이디" />
      <Input
        type="password"
        onChange={e => setUserPW(e.target.value)}
        placeholder="비밀번호"
        value={userPW}
      />
      <Input
        type="password"
        onChange={e => setUserPWConf(e.target.value)}
        placeholder="비밀번호 확인"
        value={userPWConf}
      />

      {errorMsg && <FormText>{errorMsg}</FormText>}
      <Button
        color="primary"
        onClick={() => props.setPage("SignIn")}
        style={{}}
      >
        로그인
      </Button>

      <Button
        color="primary"
        onClick={handleSignUp}
        style={{}}
      >
        회원가입
      </Button>
    </div>
  );
};

export default SignupPage;
