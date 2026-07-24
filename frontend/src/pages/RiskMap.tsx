import { CircleMarker, MapContainer, Popup, TileLayer } from 'react-leaflet';
import { Card } from '../components/Card';
import type { MapPoint } from '../types';
import { formatNumber, riskColor } from '../utils';

interface RiskMapProps {
  points: MapPoint[];
}

export function RiskMap({ points }: RiskMapProps) {
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-muted">Map</p>
        <h2 className="mt-2 text-3xl font-semibold">India state risk map</h2>
      </div>

      <Card className="overflow-hidden">
        <div className="h-[620px]">
          <MapContainer center={[22.8, 79.6]} zoom={5} scrollWheelZoom className="h-full w-full">
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {points.map((point) => (
              <CircleMarker
                key={point.state}
                center={[point.latitude, point.longitude]}
                radius={point.risk_level === 'High' ? 16 : point.risk_level === 'Medium' ? 12 : 9}
                pathOptions={{
                  color: riskColor(point.risk_level),
                  fillColor: riskColor(point.risk_level),
                  fillOpacity: 0.78,
                  weight: 2
                }}
              >
                <Popup>
                  <div className="min-w-48 text-sm">
                    <p className="font-semibold text-ink">{point.state}</p>
                    <p>Current crime: {formatNumber(point.crime_count)}</p>
                    <p>Risk level: {point.risk_level}</p>
                  </div>
                </Popup>
              </CircleMarker>
            ))}
          </MapContainer>
        </div>
      </Card>

      <div className="flex flex-wrap gap-3 text-sm text-muted">
        {(['Low', 'Medium', 'High'] as const).map((risk) => (
          <span key={risk} className="inline-flex items-center gap-2 rounded-md border border-line bg-white px-3 py-2">
            <span className="h-3 w-3 rounded-full" style={{ backgroundColor: riskColor(risk) }} />
            {risk}
          </span>
        ))}
      </div>
    </div>
  );
}

