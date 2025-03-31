import { Stack } from 'expo-router';
import SensorDisplay from '../components/SensorDisplay';

export default function IndexPage() {
  return (
    <>
      <Stack.Screen options={{ headerShown: false }} />
      <SensorDisplay />
    </>
  );
}