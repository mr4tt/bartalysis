import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import RoutePlanner from './routes/RoutePlanner'
import Service from './routes/Service'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/",
        element: <RoutePlanner />
      },
      {
        path: "/service",
        element: <Service />
      },
    ]
  },
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
