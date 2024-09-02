import { useEffect, useState } from "react"
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Label,
  LabelList,
  Line,
  LineChart,
  PolarAngleAxis,
  RadialBar,
  RadialBarChart,
  Rectangle,
  ReferenceLine,
  XAxis,
  YAxis,
} from "recharts"

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "./components/ui/chart"
import { Separator } from "@/components/ui/separator"
import { formatDate, formatPercentage } from "./utils/formatters" // Add this import

interface SimulationResult {
  timestamp: string
  win_probabilities: {
    "Donald Trump": number
    "Kamala Harris": number
  }
}

const chartConfig = {
  "Donald Trump": {
    label: "Donald Trump",
    color: "hsl(0, 100%, 50%)", // Bright red
  },
  "Kamala Harris": {
    label: "Kamala Harris",
    color: "hsl(240, 100%, 50%)", // Bright blue
  },
}

function App() {
  const [chartData, setChartData] = useState<SimulationResult[]>([])

  useEffect(() => {
    fetch('/simulation_results.json')
      .then(response => response.json())
      .then(data => setChartData(data))
      .catch(error => console.error('Error fetching data:', error))
  }, [])

  const formattedData = chartData.map(result => ({
    timestamp: new Date(result.timestamp).getTime(),
    "Donald Trump": result.win_probabilities["Donald Trump"] * 100,
    "Kamala Harris": result.win_probabilities["Kamala Harris"] * 100,
  }))

  return (
    <div className="chart-wrapper mx-auto flex max-w-6xl flex-col items-center justify-center gap-6 p-6 sm:p-8">
      <div className="w-full max-w-xl mx-auto"> {/* Use max-w-xl or another width you prefer */}
        <Card className="mx-auto"> {/* Ensure the card itself is centered */}
          <CardHeader className="space-y-0 pb-2">
            <CardDescription>Election Simulation</CardDescription>
            <CardTitle className="text-4xl tabular-nums">
              Election Results
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ChartContainer config={chartConfig}>
              <BarChart
                margin={{
                  left: 0, // Adjust the margin to center the content within the card
                  right: 0,
                }}
                data={formattedData}
              >
                <Bar
                  dataKey="Donald Trump"
                  fill={chartConfig["Donald Trump"].color}
                  radius={5}
                  fillOpacity={0.6}
                  activeBar={<Rectangle fillOpacity={0.8} />}
                />
                <Bar
                  dataKey="Kamala Harris"
                  fill={chartConfig["Kamala Harris"].color}
                  radius={5}
                  fillOpacity={0.6}
                  activeBar={<Rectangle fillOpacity={0.8} />}
                />
                <XAxis
                  dataKey="timestamp"
                  tickLine={false}
                  axisLine={false}
                  tickMargin={4}
                  tickFormatter={formatDate}
                />
                <ChartTooltip 
                  content={
                    <ChartTooltipContent 
                      indicator="dot"
                      labelFormatter={(value, payload) => {
                        if (payload && payload.length > 0) {
                          return formatDate(payload[0].payload.timestamp);
                        }
                        return '';
                      }}
                      itemSorter={(a) => -a.value}
                      formatter={(value, name) => [
                        `${formatPercentage(value)}`,
                        <span key={name} style={{ color: chartConfig[name as keyof typeof chartConfig].color }}>
                          {chartConfig[name as keyof typeof chartConfig].label}
                        </span>
                      ]}
                    />
                  } 
                  cursor={false}
                  contentStyle={{ opacity: 1 }}
                />
                <ReferenceLine
                  y={50}
                  stroke="hsl(var(--muted-foreground))"
                  strokeDasharray="3 3"
                  strokeWidth={1}
                >
                  <Label
                    position="insideBottomLeft"
                    value="50% Threshold"
                    offset={10}
                    fill="hsl(var(--foreground))"
                  />
                </ReferenceLine>
              </BarChart>
            </ChartContainer>
          </CardContent>
          <CardFooter className="flex-col items-start gap-1">
            <CardDescription>
              This chart shows the win probabilities for Donald Trump and Kamala Harris over time.
            </CardDescription>
          </CardFooter>
        </Card>
      </div>
    </div>
  )  
}

export default App