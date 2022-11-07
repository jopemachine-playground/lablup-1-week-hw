import React, { useState, useEffect } from "react";
import styled from "styled-components";

import ChattingRoomPage from "./pages/chattingRoom";
import SignInPage from "./pages/signin";
import SignUpPage from "./pages/signup";
import {parseCookie} from './utils';

const INITIAL_PAGE = "SignIn";

const App = () => {
  const [page, setPage] = useState(INITIAL_PAGE);

  useEffect(() => {
    const userId = parseCookie(document.cookie)['user_id'];
    if (userId) {
      setPage('ChattingRoom');
    }
  }, []);

  let main;
  switch (page) {
    case "ChattingRoom":
      main = <ChattingRoomPage setPage={setPage} />;
      break;
    case "SignIn":
      main = <SignInPage setPage={setPage} />;
      break;
    case "SignUp":
      main = <SignUpPage setPage={setPage} />;
      break;
    default:
      console.error('Error, page is not valid value, page: ', page);
      break;
  }

  return (
    <OuterContainer>
      {main}
    </OuterContainer>
  );
};

const OuterContainer = styled.div`
  width: 100%;
  height: 100%;
  flex: 1;
  display: flex;
  flex-direction: row;
`;

export default App;
