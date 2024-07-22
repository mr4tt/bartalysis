import { render, screen } from '@testing-library/react';
import RoutePlanner from "../src/routes/RoutePlanner"
import React from 'react';
import { describe, it, expect } from 'vitest';
import userEvent from "@testing-library/user-event";

describe("RoutePlanner", () => {
    it("renders RoutePlanner", () => {
        // since screen does not have the container property, we'll destructure render to obtain a container for this test
        const { container } = render(<RoutePlanner />);
        expect(container).toMatchSnapshot();
    });

    // it("checks user interactions", async() => {
    //     const user = userEvent.setup()
    //     render(<RoutePlanner />)
    //     const originForm = screen.getByRole("combobox", { name: "Select"})
    //     await user.selectOptions(originForm, ["Fremont"]); 

    // })
})