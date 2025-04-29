import React, { useEffect, useState } from 'react';
import {
  SafeAreaView,
  Text,
  StyleSheet,
  View,
  ActivityIndicator,
  ScrollView,
  TouchableOpacity,
  Alert
} from 'react-native';
import axios from 'axios';
import { MaterialCommunityIcons } from '@expo/vector-icons';

export default function SensorDisplay() {
  const [sensorData, setSensorData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const response = await axios.get('https://xqf3b19ksf.execute-api.us-east-2.amazonaws.com/sensor');
      setSensorData(response.data);
    } catch (error) {
      console.error('Error fetching sensor data:', error);
    } finally {
      setLoading(false);
    }
  };

  const sendControlSignal = async () => {
    try {
      await axios.post('https://xqf3b19ksf.execute-api.us-east-2.amazonaws.com/control', {
        command: 'unlock',
      });
      Alert.alert('Success', 'Control signal sent to device!');
    } catch (err) {
      console.error(err);
      Alert.alert('Error', 'Failed to send signal to ESP.');
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 1000);
    return () => clearInterval(interval);
  }, []);

  const formatTimestamp = (ts) => {
    if (!ts) return '';
    const date = new Date(ts);
    return date.toLocaleString(undefined, {
      weekday: 'long',
      month: 'long',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric'
    });
  };

  const getThermometerColor = (temp) => {
    if (temp > 85) return 'red';
    if (temp > 70) return 'orange';
    return 'blue';
  };

  const renderReedCard = (label, value, iconName) => {
    let icon = iconName;
    if (iconName === 'garage') {
      icon = 'garage';
    } else {
      icon = value === 'closed' ? `${iconName}-closed` : `${iconName}-open`;
    }

    return (
      <View style={styles.gridItem}>
        <MaterialCommunityIcons
          name={icon}
          size={40}
          color={value === 'closed' ? '#4CAF50' : '#E53935'}
        />
        <Text style={styles.label}>{label}</Text>
        <Text style={styles.value}>{value}</Text>
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.header}>Home Security Monitor</Text>

      {loading ? (
        <ActivityIndicator size="large" color="#003B73" />
      ) : sensorData ? (
        <ScrollView>
          <View style={styles.thermoCard}>
            <MaterialCommunityIcons
              name="thermometer"
              size={48}
              color={getThermometerColor(sensorData.temp)}
            />
            <Text style={styles.sectionTitle}>Temperature</Text>
            <Text style={styles.tempText}>{sensorData.temp} °F</Text>
          </View>

          <View style={styles.gridContainer}>
            {renderReedCard('Front Door', sensorData.reed_front, 'door')}
            {renderReedCard('Back Door', sensorData.reed_back, 'door')}
            {renderReedCard('Garage Door', sensorData.reed_garage, 'garage')}
            {renderReedCard('Window', sensorData.reed_window, 'window')}
          </View>

          <TouchableOpacity style={styles.controlButton} onPress={sendControlSignal}>
            <Text style={styles.buttonText}>Open Garage Door</Text>
          </TouchableOpacity>

          <Text style={styles.timestamp}>
            Last updated: {formatTimestamp(sensorData.timestamp)}
          </Text>
        </ScrollView>
      ) : (
        <Text style={styles.label}>No sensor data available.</Text>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#D6ECFA',
    paddingTop: 60,
    paddingHorizontal: 20,
  },
  header: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#003B73',
    textAlign: 'center',
    marginBottom: 20,
    marginTop: 90,
  },
  thermoCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  sectionTitle: {
    fontSize: 18,
    color: '#555',
    marginTop: 6,
  },
  tempText: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#111',
    marginTop: 4,
  },
  gridContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    gap: 12,
  },
  gridItem: {
    width: '48%',
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    marginBottom: 16,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  label: {
    fontSize: 16,
    color: '#333',
    marginTop: 8,
  },
  value: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#111',
    marginTop: 4,
  },
  timestamp: {
    marginTop: 16,
    fontSize: 14,
    color: '#888',
    textAlign: 'center',
  },
  controlButton: {
    backgroundColor: '#007AFF',
    padding: 16,
    marginTop: 20,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 30,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
