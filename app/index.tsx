import { Stack } from 'expo-router';
import React, { useState } from 'react';
import SensorDisplay from '../components/SensorDisplay';
import LoginScreen from '../components/LoginScreen';

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return isLoggedIn ? (
    <SensorDisplay />
  ) : (
    <LoginScreen onLogin={() => setIsLoggedIn(true)} />
  );
}
