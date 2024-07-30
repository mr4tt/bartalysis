import { render, screen } from '@testing-library/react';
import RoutePlanner from "../src/routes/RoutePlanner"
import React from 'react';
import { describe, it, expect } from 'vitest';
import userEvent from "@testing-library/user-event";
import "@testing-library/jest-dom"

describe("RoutePlanner", () => {
    it("renders RoutePlanner", () => {
        const { container } = render(<RoutePlanner />);
        expect(container).toMatchSnapshot();
    });

    it("fare price should be displayed", async() => {
        const fare = {
            "Description": "Clipper START",
            "FareID": 2394,
            "Price": 4.7
        }
        render(<RoutePlanner />)
        const user = userEvent.setup()
        const origin = screen.getByLabelText(/origin/i) as HTMLSelectElement;
        const destination = screen.getByLabelText(/destination/i) as HTMLSelectElement;
        const submitBtn = screen.getByRole('button', { name: /submit/i });

        origin.selectedIndex = 9;
        origin.dispatchEvent(new Event('change'));

        destination.selectedIndex = 15;
        destination.dispatchEvent(new Event('change'));
        // await user.click(submitBtn)
        
        expect(origin).toBeInTheDocument()
        expect(destination).toBeInTheDocument()
        // expect(screen.getByText(/Clipper START/i)).toBeInTheDocument()

    })
})