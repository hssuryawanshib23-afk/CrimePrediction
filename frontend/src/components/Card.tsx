import type { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
}

export function Card({ children, className = '' }: CardProps) {
  return <section className={`rounded-lg border border-line bg-panel shadow-soft ${className}`}>{children}</section>;
}

