import React, { useState } from 'react';
import SignIn from './SignIn';
import SignUp from './SignUp';

function Auth({ onAuthSuccess }) {
  const [authMode, setAuthMode] = useState('signin'); // 'signin' or 'signup'

  const handleSignInSuccess = () => {
    console.log('Sign in successful');
    onAuthSuccess && onAuthSuccess();
  };

  const handleSignUpSuccess = () => {
    console.log('Sign up successful');
    onAuthSuccess && onAuthSuccess();
  };

  return (
    <div className="landing-page">
      {authMode === 'signin' ? (
        <SignIn 
          onSwitchToSignUp={() => setAuthMode('signup')}
          onSignInSuccess={handleSignInSuccess}
        />
      ) : (
        <SignUp 
          onSwitchToSignIn={() => setAuthMode('signin')}
          onSignUpSuccess={handleSignUpSuccess}
        />
      )}
    </div>
  );
}

export default Auth;
