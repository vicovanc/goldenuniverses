/**
 * ResultsCharts - Interactive visualizations
 * GU-038: Interactive Charts
 * - Bar charts for comparisons
 * - Line charts for trends
 * - Scatter plots for correlations
 * - Log scale support
 * - Interactive tooltips
 * - Export as image (PNG/SVG)
 */

import React, { useRef, useEffect, useState } from 'react';
import * as d3 from 'd3';
import type { ResultData, ChartDataPoint } from './types';

interface ResultsChartsProps {
  results: ResultData[];
}

type ChartType = 'bar' | 'scatter' | 'precision';

export const ResultsCharts: React.FC<ResultsChartsProps> = ({ results }) => {
  const [chartType, setChartType] = useState<ChartType>('bar');
  const [logScale, setLogScale] = useState(false);
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    switch (chartType) {
      case 'bar':
        renderBarChart();
        break;
      case 'scatter':
        renderScatterPlot();
        break;
      case 'precision':
        renderPrecisionChart();
        break;
    }
  }, [results, chartType, logScale]);

  const renderBarChart = () => {
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const margin = { top: 40, right: 120, bottom: 80, left: 80 };
    const width = 900 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    const g = svg
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Prepare data - show error in ppm
    const data = results.map(r => ({
      name: r.name,
      error: Math.abs(r.errorPpm),
      category: r.category,
    })).sort((a, b) => a.error - b.error);

    // Scales
    const x = d3
      .scaleBand()
      .domain(data.map(d => d.name))
      .range([0, width])
      .padding(0.2);

    const y = logScale
      ? d3
          .scaleLog()
          .domain([0.01, d3.max(data, d => d.error) || 1])
          .range([height, 0])
          .nice()
      : d3
          .scaleLinear()
          .domain([0, d3.max(data, d => d.error) || 1])
          .range([height, 0])
          .nice();

    const colorScale = d3
      .scaleOrdinal<string>()
      .domain(['leptons', 'quarks', 'bosons', 'constants'])
      .range(['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']);

    // Add bars
    const tooltip = d3
      .select('body')
      .append('div')
      .attr('class', 'chart-tooltip')
      .style('opacity', 0)
      .style('position', 'absolute')
      .style('background', 'rgba(0, 0, 0, 0.8)')
      .style('color', 'white')
      .style('padding', '8px 12px')
      .style('border-radius', '4px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('z-index', '1000');

    g.selectAll('.bar')
      .data(data)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', d => x(d.name) || 0)
      .attr('y', d => y(d.error))
      .attr('width', x.bandwidth())
      .attr('height', d => height - y(d.error))
      .attr('fill', d => colorScale(d.category))
      .attr('opacity', 0.8)
      .on('mouseover', (event, d) => {
        tooltip.transition().duration(200).style('opacity', 0.9);
        tooltip
          .html(
            `<strong>${d.name}</strong><br/>Error: ${d.error.toFixed(3)} ppm<br/>Category: ${d.category}`
          )
          .style('left', event.pageX + 10 + 'px')
          .style('top', event.pageY - 28 + 'px');
      })
      .on('mouseout', () => {
        tooltip.transition().duration(500).style('opacity', 0);
      });

    // X axis
    g.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x))
      .selectAll('text')
      .attr('transform', 'rotate(-45)')
      .style('text-anchor', 'end')
      .style('font-size', '10px');

    // Y axis
    g.append('g')
      .call(logScale ? d3.axisLeft(y).ticks(5, '.2s') : d3.axisLeft(y))
      .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', -60)
      .attr('x', -height / 2)
      .attr('fill', 'currentColor')
      .style('text-anchor', 'middle')
      .style('font-size', '12px')
      .text('Error (ppm)');

    // Title
    g.append('text')
      .attr('x', width / 2)
      .attr('y', -10)
      .attr('text-anchor', 'middle')
      .style('font-size', '16px')
      .style('font-weight', 'bold')
      .text('Precision by Quantity');

    // Legend
    const legend = g
      .append('g')
      .attr('class', 'legend')
      .attr('transform', `translate(${width + 20}, 0)`);

    const categories = ['leptons', 'quarks', 'bosons', 'constants'];
    categories.forEach((cat, i) => {
      const legendRow = legend
        .append('g')
        .attr('transform', `translate(0, ${i * 25})`);

      legendRow
        .append('rect')
        .attr('width', 15)
        .attr('height', 15)
        .attr('fill', colorScale(cat));

      legendRow
        .append('text')
        .attr('x', 20)
        .attr('y', 12)
        .style('font-size', '12px')
        .text(cat);
    });
  };

  const renderScatterPlot = () => {
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const margin = { top: 40, right: 40, bottom: 60, left: 80 };
    const width = 900 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    const g = svg
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Prepare data
    const data = results.map((r, i) => ({
      x: i,
      y: Math.abs(r.errorPpm),
      name: r.name,
      category: r.category,
      theoretical: r.theoretical,
    }));

    // Scales
    const x = d3
      .scaleLinear()
      .domain([0, data.length - 1])
      .range([0, width]);

    const y = logScale
      ? d3
          .scaleLog()
          .domain([0.01, d3.max(data, d => d.y) || 1])
          .range([height, 0])
          .nice()
      : d3
          .scaleLinear()
          .domain([0, d3.max(data, d => d.y) || 1])
          .range([height, 0])
          .nice();

    const colorScale = d3
      .scaleOrdinal<string>()
      .domain(['leptons', 'quarks', 'bosons', 'constants'])
      .range(['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']);

    // Add circles
    const tooltip = d3
      .select('body')
      .append('div')
      .attr('class', 'chart-tooltip')
      .style('opacity', 0)
      .style('position', 'absolute')
      .style('background', 'rgba(0, 0, 0, 0.8)')
      .style('color', 'white')
      .style('padding', '8px 12px')
      .style('border-radius', '4px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('z-index', '1000');

    g.selectAll('.dot')
      .data(data)
      .enter()
      .append('circle')
      .attr('class', 'dot')
      .attr('cx', d => x(d.x))
      .attr('cy', d => y(d.y))
      .attr('r', 6)
      .attr('fill', d => colorScale(d.category))
      .attr('opacity', 0.7)
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .on('mouseover', (event, d) => {
        tooltip.transition().duration(200).style('opacity', 0.9);
        tooltip
          .html(
            `<strong>${d.name}</strong><br/>Error: ${d.y.toFixed(3)} ppm<br/>Category: ${d.category}`
          )
          .style('left', event.pageX + 10 + 'px')
          .style('top', event.pageY - 28 + 'px');
      })
      .on('mouseout', () => {
        tooltip.transition().duration(500).style('opacity', 0);
      });

    // Add reference lines
    const referenceLines = [1, 10, 100];
    referenceLines.forEach(value => {
      if (value <= (d3.max(data, d => d.y) || 1)) {
        g.append('line')
          .attr('x1', 0)
          .attr('x2', width)
          .attr('y1', y(value))
          .attr('y2', y(value))
          .attr('stroke', '#999')
          .attr('stroke-dasharray', '4 4')
          .attr('opacity', 0.3);

        g.append('text')
          .attr('x', width - 5)
          .attr('y', y(value) - 5)
          .attr('text-anchor', 'end')
          .style('font-size', '10px')
          .style('fill', '#999')
          .text(`${value} ppm`);
      }
    });

    // Axes
    g.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x).ticks(0));

    g.append('g')
      .call(logScale ? d3.axisLeft(y).ticks(5, '.2s') : d3.axisLeft(y))
      .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', -60)
      .attr('x', -height / 2)
      .attr('fill', 'currentColor')
      .style('text-anchor', 'middle')
      .style('font-size', '12px')
      .text('Error (ppm)');

    // Title
    g.append('text')
      .attr('x', width / 2)
      .attr('y', -10)
      .attr('text-anchor', 'middle')
      .style('font-size', '16px')
      .style('font-weight', 'bold')
      .text('Precision Distribution');
  };

  const renderPrecisionChart = () => {
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const margin = { top: 40, right: 40, bottom: 60, left: 80 };
    const width = 900 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    const g = svg
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Bin data by precision ranges
    const bins = [
      { range: '< 1 ppm', count: 0, color: '#00C853' },
      { range: '1-10 ppm', count: 0, color: '#64DD17' },
      { range: '10-100 ppm', count: 0, color: '#FFD600' },
      { range: '100-1000 ppm', count: 0, color: '#FF9100' },
      { range: '> 1000 ppm', count: 0, color: '#FF3D00' },
    ];

    results.forEach(r => {
      const ppm = Math.abs(r.errorPpm);
      if (ppm < 1) bins[0].count++;
      else if (ppm < 10) bins[1].count++;
      else if (ppm < 100) bins[2].count++;
      else if (ppm < 1000) bins[3].count++;
      else bins[4].count++;
    });

    // Scales
    const x = d3
      .scaleBand()
      .domain(bins.map(d => d.range))
      .range([0, width])
      .padding(0.3);

    const y = d3
      .scaleLinear()
      .domain([0, d3.max(bins, d => d.count) || 1])
      .range([height, 0])
      .nice();

    // Add bars
    g.selectAll('.bar')
      .data(bins)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', d => x(d.range) || 0)
      .attr('y', d => y(d.count))
      .attr('width', x.bandwidth())
      .attr('height', d => height - y(d.count))
      .attr('fill', d => d.color)
      .attr('opacity', 0.8);

    // Add count labels
    g.selectAll('.label')
      .data(bins)
      .enter()
      .append('text')
      .attr('class', 'label')
      .attr('x', d => (x(d.range) || 0) + x.bandwidth() / 2)
      .attr('y', d => y(d.count) - 5)
      .attr('text-anchor', 'middle')
      .style('font-size', '14px')
      .style('font-weight', 'bold')
      .text(d => d.count);

    // Axes
    g.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x))
      .selectAll('text')
      .style('font-size', '11px');

    g.append('g')
      .call(d3.axisLeft(y).ticks(5))
      .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', -60)
      .attr('x', -height / 2)
      .attr('fill', 'currentColor')
      .style('text-anchor', 'middle')
      .style('font-size', '12px')
      .text('Number of Results');

    // Title
    g.append('text')
      .attr('x', width / 2)
      .attr('y', -10)
      .attr('text-anchor', 'middle')
      .style('font-size', '16px')
      .style('font-weight', 'bold')
      .text('Precision Distribution');
  };

  const exportChart = (format: 'png' | 'svg') => {
    if (!svgRef.current) return;

    if (format === 'svg') {
      const svgData = new XMLSerializer().serializeToString(svgRef.current);
      const blob = new Blob([svgData], { type: 'image/svg+xml' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `golden-universe-chart.svg`;
      link.click();
      URL.revokeObjectURL(url);
    } else {
      // PNG export (requires canvas)
      const svgData = new XMLSerializer().serializeToString(svgRef.current);
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new Image();

      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx?.drawImage(img, 0, 0);
        canvas.toBlob(blob => {
          if (blob) {
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `golden-universe-chart.png`;
            link.click();
            URL.revokeObjectURL(url);
          }
        });
      };

      img.src = 'data:image/svg+xml;base64,' + btoa(svgData);
    }
  };

  return (
    <div className="results-charts">
      <div className="charts-header">
        <h3>Interactive Visualizations</h3>
        <div className="chart-controls">
          <div className="chart-type-selector">
            <button
              className={chartType === 'bar' ? 'active' : ''}
              onClick={() => setChartType('bar')}
            >
              Bar Chart
            </button>
            <button
              className={chartType === 'scatter' ? 'active' : ''}
              onClick={() => setChartType('scatter')}
            >
              Scatter Plot
            </button>
            <button
              className={chartType === 'precision' ? 'active' : ''}
              onClick={() => setChartType('precision')}
            >
              Precision Bins
            </button>
          </div>
          <label className="log-scale-toggle">
            <input
              type="checkbox"
              checked={logScale}
              onChange={e => setLogScale(e.target.checked)}
              disabled={chartType === 'precision'}
            />
            Log Scale
          </label>
          <div className="export-buttons">
            <button onClick={() => exportChart('png')}>Export PNG</button>
            <button onClick={() => exportChart('svg')}>Export SVG</button>
          </div>
        </div>
      </div>

      <div className="chart-container">
        <svg ref={svgRef}></svg>
      </div>
    </div>
  );
};
