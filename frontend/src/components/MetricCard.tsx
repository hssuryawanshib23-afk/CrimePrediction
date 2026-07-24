interface MetricCardProps {
  label: string;
  value: string;
  detail?: string;
}

export function MetricCard({ label, value, detail }: MetricCardProps) {
  return (
    <div className="rounded-lg border border-line bg-white p-5 shadow-soft">
      <p className="text-sm font-medium text-muted">{label}</p>
      <p className="mt-2 text-3xl font-semibold tracking-normal text-ink">{value}</p>
      {detail ? <p className="mt-2 text-sm text-muted">{detail}</p> : null}
    </div>
  );
}

