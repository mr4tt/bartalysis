import React from "react"
import { Link } from 'react-router-dom';

export default function Nav() {

    return (
        <div className=" bg-blue-300 text-black row-span-1 w-screen flex items-center justify-between px-8 py-4 text-xl">
            <div className="justify-self-start flex gap-24">
                <Link to="/" className="hover:underline">Home</Link>
                <Link to="/service" className="hover:underline">Service</Link>

            </div>
            <div className="">Logo placeholder</div>
        </div>
    )
}