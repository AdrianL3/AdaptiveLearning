// src/features/auth/auth.js
import { createUserWithEmailAndPassword } from "firebase/auth";
import { auth } from './firebase';  // Import the auth instance

export const createUserWithEmailAndPasswordFn = async (email, password) => { // ADDED FN
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    return userCredential.user;
  } catch (error) {
    console.error("Error creating user:", error.message);
    throw error;
  }
};
