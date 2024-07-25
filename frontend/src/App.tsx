import React from 'react';
import Nav from './components/Nav';
import { Outlet } from 'react-router-dom';

// root element
function App() {
  return (
    <div className="h-screen grid grid-rows-8 ">
      <Nav />
      <Outlet />
    </div>
  );
}

export default App;
