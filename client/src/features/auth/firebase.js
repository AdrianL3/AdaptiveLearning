// src/features/auth/firebase.js
import { initializeApp } from 'firebase/app';
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCAE3u91Axx1viYaCdO2mMtx4vp24_tquo",
  authDomain: "adaptivelearning-8b398.firebaseapp.com",
  projectId: "adaptivelearning-8b398",
  storageBucket: "adaptivelearning-8b398.firebasestorage.app",
  messagingSenderId: "640657589590",
  appId: "1:640657589590:web:03028de20b7ac4d09002f7",
  measurementId: "G-PTCJFTF2XF"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

export default app;
