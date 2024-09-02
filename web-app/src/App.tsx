import { useEffect, useState, useMemo } from "react"
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs"
import { Slider } from "./components/ui/slider"

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
  const [daysToShow, setDaysToShow] = useState(10) // Default to showing 10 days

  useEffect(() => {
    fetch('/simulation_results.json')
      .then(response => response.json())
      .then(data => setChartData(data))
      .catch(error => console.error('Error fetching data:', error))
  }, [])

  const formattedData = useMemo(() => {
    const dailyData: { [key: string]: { sum: { [key: string]: number }, count: number } } = {}

    chartData.forEach(result => {
      const date = new Date(result.timestamp).toDateString()
      if (!dailyData[date]) {
        dailyData[date] = { sum: { "Donald Trump": 0, "Kamala Harris": 0 }, count: 0 }
      }
      dailyData[date].sum["Donald Trump"] += result.win_probabilities["Donald Trump"]
      dailyData[date].sum["Kamala Harris"] += result.win_probabilities["Kamala Harris"]
      dailyData[date].count++
    })

    return Object.entries(dailyData).map(([date, data]) => ({
      timestamp: new Date(date).getTime(),
      "Donald Trump": (data.sum["Donald Trump"] / data.count) * 100,
      "Kamala Harris": (data.sum["Kamala Harris"] / data.count) * 100,
    })).sort((a, b) => a.timestamp - b.timestamp)
  }, [chartData])

  const filteredData = useMemo(() => {
    const cutoffDate = new Date()
    cutoffDate.setDate(cutoffDate.getDate() - daysToShow)
    return formattedData.filter(data => data.timestamp >= cutoffDate.getTime())
  }, [formattedData, daysToShow])

  const renderChart = (ChartComponent: typeof BarChart | typeof LineChart) => (
    <ChartContainer config={chartConfig}>
      <ChartComponent
        margin={{
          left: 0,
          right: 0,
        }}
        data={filteredData}
      >
        {ChartComponent === LineChart && <CartesianGrid vertical={false} />}
        <XAxis
          dataKey="timestamp"
          tickLine={false}
          axisLine={false}
          tickMargin={8}
          tickFormatter={formatDate}
        />
        {ChartComponent === LineChart && (
          <YAxis
            tickLine={false}
            axisLine={false}
            tickMargin={8}
            tickFormatter={(value) => `${value}%`}
          />
        )}
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
          cursor={ChartComponent === BarChart ? false : undefined}
        />
        {ChartComponent === BarChart ? (
          <>
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
          </>
        ) : (
          <>
            <Line
              type="monotone"
              dataKey="Donald Trump"
              stroke={chartConfig["Donald Trump"].color}
              strokeWidth={2}
              dot={false}
            />
            <Line
              type="monotone"
              dataKey="Kamala Harris"
              stroke={chartConfig["Kamala Harris"].color}
              strokeWidth={2}
              dot={false}
            />
          </>
        )}
        <ReferenceLine
          y={50}
          stroke="hsl(var(--foreground) / 0.3)"
          strokeDasharray="3 3"
          strokeWidth={2}
        >
          <Label
            position="insideBottomLeft"
            value="50% Threshold"
            offset={10}
            fill="hsl(var(--foreground) / 0.5)"
          />
        </ReferenceLine>
      </ChartComponent>
    </ChartContainer>
  )

  return (
    <div className="min-h-screen bg-background bg-gray-100">
      <div 
        className="bg-blue-100 w-full" 
        style={{
          maxWidth: '672px', 
          margin: '0 auto', 
          padding: '2rem 1rem',
        }}
      >
        <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight text-center lg:text-5xl mb-6">
          2024 Election Simulation
        </h1>
        <p className="leading-7 text-center mb-8">
          This simulation provides daily win probabilities for the potential candidates in the upcoming 2024 US Presidential Election. The data is based on various factors and is updated regularly to reflect the latest trends and developments.
        </p>
        
        <Card className="rounded-lg mb-10">
          <CardHeader className="space-y-0 pb-2">
            <CardDescription>Election Simulation</CardDescription>
            <CardTitle className="text-4xl tabular-nums">
              Win Probabilities
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="bar">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="bar">Bar Chart</TabsTrigger>
                <TabsTrigger value="line">Line Chart</TabsTrigger>
              </TabsList>
              <TabsContent value="bar">
                {renderChart(BarChart)}
              </TabsContent>
              <TabsContent value="line">
                {renderChart(LineChart)}
              </TabsContent>
            </Tabs>
            <div className="mt-4 flex flex-col items-center">
              <label htmlFor="days-slider" className="block text-sm font-medium text-gray-700 mb-2">
                Days to show: {daysToShow}
              </label>
              {/* Option 1: Inline styles */}
              <div style={{ width: '256px' }}>
                <Slider
                  id="days-slider"
                  min={5}
                  max={formattedData.length}
                  step={1}
                  value={[daysToShow]}
                  onValueChange={(value) => setDaysToShow(value[0])}
                />
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex-col items-start gap-1">
            <CardDescription>
              This chart shows the average daily win probabilities for Donald Trump and Kamala Harris over the last {daysToShow} days.
            </CardDescription>
          </CardFooter>
        </Card>
        
        <h2 className="mt-10 scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight transition-colors first:mt-0">
          Understanding the Data
        </h2>
        <p className="leading-7 [&:not(:first-child)]:mt-6">
          The chart above displays the average daily win probabilities for Donald Trump and Kamala Harris. These probabilities are calculated based on various factors including polling data, economic indicators, and historical trends.
        </p>
        <h3 className="mt-8 scroll-m-20 text-2xl font-semibold tracking-tight">
          Key Observations
        </h3>
        <ul className="my-6 ml-6 list-disc [&>li]:mt-2">
          <li>The 50% threshold line represents an equal chance of winning for both candidates.</li>
          <li>Probabilities above 50% indicate a higher likelihood of winning for that candidate.</li>
          <li>Daily fluctuations are normal and can be influenced by current events and news cycles.</li>
        </ul>
        <p className="leading-7 [&:not(:first-child)]:mt-6">
          Remember, these simulations are based on current data and projections. The actual election outcome may differ as we get closer to the election date and more information becomes available.
        </p>
      </div>
    </div>
  )
}

export default App