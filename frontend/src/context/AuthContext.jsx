import { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const id   = localStorage.getItem('customerId');
    const name = localStorage.getItem('customerName');
    return id ? { id: parseInt(id, 10), name } : null;
  });

  const login = (userData) => {
    localStorage.setItem('customerId',   String(userData.customer_id));
    localStorage.setItem('customerName', userData.name);
    setUser({ id: userData.customer_id, name: userData.name });
  };

  const logout = () => {
    localStorage.removeItem('customerId');
    localStorage.removeItem('customerName');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
