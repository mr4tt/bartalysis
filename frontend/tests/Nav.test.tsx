import { render, screen } from '@testing-library/react';
import React from 'react';
import { describe, it, expect, beforeEach, } from 'vitest';
import "@testing-library/jest-dom"
import Nav from "../src/components/Nav"
import { Router } from 'react-router-dom';
import {  createMemoryHistory } from 'history';
import userEvent from "@testing-library/user-event";

describe("Nav.tsx", () => {
    const history = createMemoryHistory();
    const user = userEvent.setup();

    beforeEach(() => {
        render(
            <Router location={history.location} navigator={history}>
                <Nav />
            </Router>
        )
    })

    it("should contain Home link and work", async() => {
        await user.click(screen.getByText(/Home/i));
        expect(history.location.pathname).toBe('/');
        expect(screen.getByText("Home")).toBeInTheDocument()
        expect(screen.getByText("Home")).toHaveTextContent(/Home/i)
    })

    it("should contain Service link and work", async() => {
        await user.click(screen.getByText(/Service/i));
        expect(history.location.pathname).toBe('/service');
        expect(screen.getByText("Service")).toBeInTheDocument()
        expect(screen.getByText("Service")).toHaveTextContent(/Service/i)
    })
})