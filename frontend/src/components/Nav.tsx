import React from "react"
import { Link } from 'react-router-dom';

export default function Nav() {

    return (
        <div className=" row-span-1 bg-slate-400 w-screen flex items-center justify-between px-8 py-4">
            <Link to="/" className="hover:underline">Home</Link>
            <Link to="/service" className="hover:underline">Service</Link>
            <Link to="/map" className="hover:underline">Map</Link>
            <div>Logo placeholder</div>
        </div>
    )
}