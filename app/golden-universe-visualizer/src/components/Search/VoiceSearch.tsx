/**
 * VoiceSearch Component - GU-030: Voice Search
 *
 * Features:
 * - Microphone permission request
 * - Speech-to-text conversion
 * - Visual feedback during recording
 * - Error handling
 * - Cross-browser support using Web Speech API
 */

import React, { useState, useEffect, useRef } from 'react';

interface VoiceSearchProps {
  onResult: (transcript: string) => void;
  onError?: (error: string) => void;
}

// Check if browser supports Web Speech API
const isSpeechRecognitionSupported = (): boolean => {
  return (
    'webkitSpeechRecognition' in window ||
    'SpeechRecognition' in window
  );
};

// Get the SpeechRecognition class
const getSpeechRecognition = (): typeof SpeechRecognition | null => {
  if ('webkitSpeechRecognition' in window) {
    return (window as any).webkitSpeechRecognition;
  } else if ('SpeechRecognition' in window) {
    return (window as any).SpeechRecognition;
  }
  return null;
};

const VoiceSearch: React.FC<VoiceSearchProps> = ({ onResult, onError }) => {
  const [isListening, setIsListening] = useState<boolean>(false);
  const [isSupported, setIsSupported] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [transcript, setTranscript] = useState<string>('');
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // Check browser support
    const supported = isSpeechRecognitionSupported();
    setIsSupported(supported);

    if (!supported) {
      const errorMsg = 'Voice search is not supported in this browser';
      setError(errorMsg);
      console.warn(errorMsg);
      return;
    }

    // Initialize Speech Recognition
    const SpeechRecognitionClass = getSpeechRecognition();
    if (!SpeechRecognitionClass) {
      return;
    }

    const recognition = new SpeechRecognitionClass();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    // Handle results
    recognition.onresult = (event: any) => {
      let interimTranscript = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcriptPart = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcriptPart;
        } else {
          interimTranscript += transcriptPart;
        }
      }

      // Update transcript display
      const currentTranscript = finalTranscript || interimTranscript;
      setTranscript(currentTranscript);

      // If final result, send to parent
      if (finalTranscript) {
        onResult(finalTranscript);
        setIsListening(false);
        setTranscript('');
      }
    };

    // Handle errors
    recognition.onerror = (event: any) => {
      let errorMessage = 'Voice search error';

      switch (event.error) {
        case 'no-speech':
          errorMessage = 'No speech detected. Please try again.';
          break;
        case 'audio-capture':
          errorMessage = 'No microphone found. Please check your device.';
          break;
        case 'not-allowed':
          errorMessage = 'Microphone permission denied. Please enable it in your browser settings.';
          break;
        case 'network':
          errorMessage = 'Network error. Please check your connection.';
          break;
        case 'aborted':
          errorMessage = 'Voice search was cancelled.';
          break;
        default:
          errorMessage = `Voice search error: ${event.error}`;
      }

      setError(errorMessage);
      setIsListening(false);
      setTranscript('');

      if (onError) {
        onError(errorMessage);
      }

      console.error('Speech recognition error:', event.error);
    };

    // Handle end
    recognition.onend = () => {
      setIsListening(false);
    };

    // Handle start
    recognition.onstart = () => {
      setIsListening(true);
      setError(null);
      setTranscript('');
    };

    recognitionRef.current = recognition;

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
    };
  }, [onResult, onError]);

  const startListening = async () => {
    if (!isSupported || !recognitionRef.current) {
      return;
    }

    try {
      // Request microphone permission
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      // Stop the stream immediately (we just needed permission)
      stream.getTracks().forEach(track => track.stop());

      // Start recognition
      recognitionRef.current.start();
    } catch (err: any) {
      const errorMessage = err.name === 'NotAllowedError'
        ? 'Microphone permission denied. Please enable it in your browser settings.'
        : 'Could not access microphone. Please check your device.';

      setError(errorMessage);

      if (onError) {
        onError(errorMessage);
      }

      console.error('Microphone access error:', err);
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
    }
  };

  const handleToggle = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  if (!isSupported) {
    return (
      <button
        className="voice-search voice-search--disabled"
        disabled
        title="Voice search is not supported in this browser"
        aria-label="Voice search not supported"
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 20 20"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M10 1a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"
            stroke="currentColor"
            strokeWidth="2"
            fill="none"
          />
          <path
            d="M4 10a6 6 0 0 0 12 0M10 16v3"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          />
          <path
            d="M2 2l16 16"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>
      </button>
    );
  }

  return (
    <div className="voice-search-wrapper">
      <button
        className={`voice-search ${isListening ? 'voice-search--listening' : ''} ${
          error ? 'voice-search--error' : ''
        }`}
        onClick={handleToggle}
        title={isListening ? 'Stop listening' : 'Start voice search'}
        aria-label={isListening ? 'Stop voice search' : 'Start voice search'}
      >
        {/* Microphone Icon */}
        <svg
          width="20"
          height="20"
          viewBox="0 0 20 20"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="voice-search__icon"
        >
          <path
            d="M10 1a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"
            stroke="currentColor"
            strokeWidth="2"
            fill={isListening ? 'currentColor' : 'none'}
          />
          <path
            d="M4 10a6 6 0 0 0 12 0M10 16v3"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>

        {/* Pulse animation when listening */}
        {isListening && (
          <span className="voice-search__pulse">
            <span className="voice-search__pulse-ring" />
            <span className="voice-search__pulse-ring voice-search__pulse-ring--delay" />
          </span>
        )}
      </button>

      {/* Transcript display */}
      {isListening && transcript && (
        <div className="voice-search__transcript">
          <span className="voice-search__transcript-text">{transcript}</span>
        </div>
      )}

      {/* Error message */}
      {error && !isListening && (
        <div className="voice-search__error">
          <span className="voice-search__error-icon">⚠️</span>
          <span className="voice-search__error-text">{error}</span>
        </div>
      )}

      {/* Listening indicator */}
      {isListening && (
        <div className="voice-search__indicator">
          <div className="voice-search__indicator-icon">🎤</div>
          <div className="voice-search__indicator-text">
            Listening... Speak now
          </div>
        </div>
      )}
    </div>
  );
};

export default VoiceSearch;
