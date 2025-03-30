import React, { useEffect, useState } from 'react';
import { SafeAreaView, Text, StyleSheet, ActivityIndicator, RefreshControl, ScrollView } from 'react-native';
import axios from 'axios';

export default function App() {
  const [sensorData, setSensorData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = async () => {
    try {
      const response = await axios.get('https://xqf3b19ksf.execute-api.us-east-2.amazonaws.com/sensor');
      setSensorData(response.data);
    } catch (error) {
      console.error('Error fetching sensor data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchData();
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView 
        contentContainerStyle={styles.content}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
      >
        <Text style={styles.title}>Latest Sensor Reading</Text>
        {loading ? (
          <ActivityIndicator size="large" color="#007AFF" />
        ) : sensorData && sensorData.sensor_id ? (
          <>
            <Text style={styles.label}>Sensor ID: <Text style={styles.value}>{sensorData.sensor_id}</Text></Text>
            <Text style={styles.label}>Temperature: <Text style={styles.value}>{sensorData.value} °F</Text></Text>
            <Text style={styles.label}>Timestamp: <Text style={styles.value}>{sensorData.timestamp}</Text></Text>
          </>
        ) : (
          <Text style={styles.label}>No data found.</Text>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f0f4f7' },
  content: { padding: 20, justifyContent: 'center', alignItems: 'center', flexGrow: 1 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  label: { fontSize: 18, marginVertical: 5 },
  value: { fontWeight: 'bold' },
});
