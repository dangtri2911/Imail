import React from 'react';
import { Link } from 'react-router-dom';
import SignIn from './SignIn';
function SignOut() {
    localStorage.removeItem("userName");
  return (
    <>
        <SignIn
            signOut = 'Sign out success'
        />
    </>
  );
}

export default SignOut;