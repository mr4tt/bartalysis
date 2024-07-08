import { render, screen } from '@testing-library/react';
import App from '../src/App';
import React from 'react';
import { describe, it, expect } from 'vitest';

describe('App', () => {
  it('renders headline', () => {
    render(<App />);
    expect(screen.getByRole("heading").textContent).toMatch('hi bartalysis team');
  });
});