// LoginScreen.tsx
import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet, Text, Alert } from 'react-native';

interface LoginScreenProps {
  onLogin: () => void;
}

export default function LoginScreen({ onLogin }: LoginScreenProps) {
  const [username, setUsername] = useState('');

  const handleLogin = () => {
    if (username === 'admin') {
      onLogin();
    } else {
      Alert.alert('Login Failed', 'Incorrect username.');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Home Security Login</Text>
      <TextInput
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
        style={styles.input}
      />
      <Button title="Login" onPress={handleLogin} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 24, backgroundColor: '#D6ECFA' },
  title: { fontSize: 24, textAlign: 'center', marginBottom: 20 },
  input: {
    borderWidth: 1, borderColor: '#aaa', padding: 12, marginBottom: 16, borderRadius: 8
  }
});
