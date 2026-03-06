import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { theoryLaws, lawDependencies } from '@/data/theoryLaws';
import { LawCategory } from '@/types/theory';

interface DependencyGraphProps {
  onSelectLaw?: (lawId: number) => void;
  highlightLawId?: number;
}

interface GraphNode extends d3.SimulationNodeDatum {
  id: number;
  title: string;
  category: LawCategory;
  status: string;
}

interface GraphLink extends d3.SimulationLinkDatum<GraphNode> {
  source: number | GraphNode;
  target: number | GraphNode;
  type: string;
}

const DependencyGraph: React.FC<DependencyGraphProps> = ({ onSelectLaw, highlightLawId }) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [showLabels, setShowLabels] = useState(true);

  useEffect(() => {
    if (!svgRef.current || !containerRef.current) return;

    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Clear previous graph
    d3.select(svgRef.current).selectAll('*').remove();

    // Filter nodes by category
    const filteredNodes = theoryLaws
      .filter((law) => filterCategory === 'all' || law.category === filterCategory)
      .map((law) => ({
        id: law.id,
        title: law.title,
        category: law.category,
        status: law.status,
      }));

    const nodeIds = new Set(filteredNodes.map((n) => n.id));

    // Filter links to only include nodes in the filtered set
    const filteredLinks = lawDependencies
      .filter((dep) => nodeIds.has(dep.from) && nodeIds.has(dep.to))
      .map((dep) => ({
        source: dep.from,
        target: dep.to,
        type: dep.type,
      }));

    // Create SVG
    const svg = d3
      .select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', [0, 0, width, height])
      .attr('style', 'max-width: 100%; height: auto;');

    // Add zoom behavior
    const g = svg.append('g');

    const zoom = d3
      .zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });

    svg.call(zoom);

    // Define arrow markers for different link types
    const defs = svg.append('defs');

    const linkTypes = ['uses', 'derives', 'constrains', 'validates'];
    linkTypes.forEach((type) => {
      defs
        .append('marker')
        .attr('id', `arrow-${type}`)
        .attr('viewBox', '0 -5 10 10')
        .attr('refX', 20)
        .attr('refY', 0)
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('orient', 'auto')
        .append('path')
        .attr('d', 'M0,-5L10,0L0,5')
        .attr('class', `arrow-${type}`);
    });

    // Create force simulation
    const simulation = d3
      .forceSimulation<GraphNode>(filteredNodes as GraphNode[])
      .force(
        'link',
        d3
          .forceLink<GraphNode, GraphLink>(filteredLinks as GraphLink[])
          .id((d) => d.id)
          .distance(100)
      )
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(30));

    // Create links
    const link = g
      .append('g')
      .selectAll('line')
      .data(filteredLinks)
      .join('line')
      .attr('class', (d) => `link link-${d.type}`)
      .attr('marker-end', (d) => `url(#arrow-${d.type})`)
      .attr('stroke', (d) => {
        const colors: { [key: string]: string } = {
          uses: '#4a9eff',
          derives: '#00ff88',
          constrains: '#ff6b6b',
          validates: '#ffd700',
        };
        return colors[d.type] || '#666';
      })
      .attr('stroke-width', 1.5)
      .attr('stroke-opacity', 0.6);

    // Create nodes
    const node = g
      .append('g')
      .selectAll('g')
      .data(filteredNodes)
      .join('g')
      .attr('class', (d) => `node node-${d.category} ${d.id === highlightLawId ? 'highlighted' : ''}`)
      .call(
        d3
          .drag<SVGGElement, GraphNode>()
          .on('start', dragstarted)
          .on('drag', dragged)
          .on('end', dragended)
      );

    // Add circles to nodes
    node
      .append('circle')
      .attr('r', 12)
      .attr('fill', (d) => {
        const colors: { [key: string]: string } = {
          foundation: '#ff6b6b',
          symmetry: '#4ecdc4',
          particles: '#45b7d1',
          advanced: '#96ceb4',
        };
        return colors[d.category] || '#666';
      })
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .attr('class', (d) => (d.id === highlightLawId ? 'node-circle-highlighted' : ''));

    // Add labels
    const labels = node
      .append('text')
      .text((d) => `${d.id}`)
      .attr('x', 0)
      .attr('y', 4)
      .attr('text-anchor', 'middle')
      .attr('class', 'node-label')
      .style('font-size', '10px')
      .style('font-weight', 'bold')
      .style('fill', '#fff')
      .style('pointer-events', 'none');

    // Add title labels (shown on hover or when enabled)
    const titleLabels = node
      .append('text')
      .text((d) => d.title.substring(0, 30) + (d.title.length > 30 ? '...' : ''))
      .attr('x', 18)
      .attr('y', 4)
      .attr('class', 'node-title-label')
      .style('font-size', '11px')
      .style('fill', '#ccc')
      .style('pointer-events', 'none')
      .style('display', showLabels ? 'block' : 'none');

    // Add tooltips
    node.append('title').text((d) => `Law ${d.id}: ${d.title}\nStatus: ${d.status}\nCategory: ${d.category}`);

    // Highlight connected nodes on hover
    node
      .on('mouseenter', function (event, d) {
        // Highlight connected nodes
        const connectedIds = new Set<number>();
        connectedIds.add(d.id);

        filteredLinks.forEach((link) => {
          const sourceId = typeof link.source === 'number' ? link.source : link.source.id;
          const targetId = typeof link.target === 'number' ? link.target : link.target.id;

          if (sourceId === d.id) connectedIds.add(targetId);
          if (targetId === d.id) connectedIds.add(sourceId);
        });

        node.style('opacity', (n) => (connectedIds.has(n.id) ? 1 : 0.2));
        link.style('opacity', (l) => {
          const sourceId = typeof l.source === 'number' ? l.source : l.source.id;
          const targetId = typeof l.target === 'number' ? l.target : l.target.id;
          return connectedIds.has(sourceId) && connectedIds.has(targetId) ? 1 : 0.1;
        });
      })
      .on('mouseleave', function () {
        node.style('opacity', 1);
        link.style('opacity', 0.6);
      })
      .on('click', (event, d) => {
        if (onSelectLaw) {
          onSelectLaw(d.id);
        }
      });

    // Update positions on tick
    simulation.on('tick', () => {
      link
        .attr('x1', (d) => (typeof d.source === 'number' ? 0 : d.source.x || 0))
        .attr('y1', (d) => (typeof d.source === 'number' ? 0 : d.source.y || 0))
        .attr('x2', (d) => (typeof d.target === 'number' ? 0 : d.target.x || 0))
        .attr('y2', (d) => (typeof d.target === 'number' ? 0 : d.target.y || 0));

      node.attr('transform', (d) => `translate(${d.x || 0},${d.y || 0})`);
    });

    // Drag functions
    function dragstarted(event: d3.D3DragEvent<SVGGElement, GraphNode, GraphNode>) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event: d3.D3DragEvent<SVGGElement, GraphNode, GraphNode>) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragended(event: d3.D3DragEvent<SVGGElement, GraphNode, GraphNode>) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    return () => {
      simulation.stop();
    };
  }, [filterCategory, highlightLawId, onSelectLaw, showLabels]);

  // Export as SVG
  const exportSVG = () => {
    if (!svgRef.current) return;

    const svgData = new XMLSerializer().serializeToString(svgRef.current);
    const blob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = 'theory-dependency-graph.svg';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Export as PNG
  const exportPNG = () => {
    if (!svgRef.current) return;

    const svgData = new XMLSerializer().serializeToString(svgRef.current);
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();

    const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(svgBlob);

    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx?.drawImage(img, 0, 0);
      URL.revokeObjectURL(url);

      canvas.toBlob((blob) => {
        if (blob) {
          const pngUrl = URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = pngUrl;
          link.download = 'theory-dependency-graph.png';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          URL.revokeObjectURL(pngUrl);
        }
      });
    };

    img.src = url;
  };

  return (
    <div className="dependency-graph">
      <div className="graph-controls">
        <div className="filter-controls">
          <label>
            Category Filter:
            <select value={filterCategory} onChange={(e) => setFilterCategory(e.target.value)}>
              <option value="all">All Categories</option>
              <option value="foundation">Foundation</option>
              <option value="symmetry">Symmetry</option>
              <option value="particles">Particles</option>
              <option value="advanced">Advanced</option>
            </select>
          </label>
          <label className="checkbox-label">
            <input type="checkbox" checked={showLabels} onChange={(e) => setShowLabels(e.target.checked)} />
            Show Labels
          </label>
        </div>
        <div className="export-controls">
          <button onClick={exportSVG} className="export-button">
            Export SVG
          </button>
          <button onClick={exportPNG} className="export-button">
            Export PNG
          </button>
        </div>
      </div>
      <div className="graph-legend">
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#ff6b6b' }}></div>
          <span>Foundation</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#4ecdc4' }}></div>
          <span>Symmetry</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#45b7d1' }}></div>
          <span>Particles</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#96ceb4' }}></div>
          <span>Advanced</span>
        </div>
        <div className="legend-divider"></div>
        <div className="legend-item">
          <div className="legend-line" style={{ borderColor: '#4a9eff' }}></div>
          <span>Uses</span>
        </div>
        <div className="legend-item">
          <div className="legend-line" style={{ borderColor: '#00ff88' }}></div>
          <span>Derives</span>
        </div>
        <div className="legend-item">
          <div className="legend-line" style={{ borderColor: '#ff6b6b' }}></div>
          <span>Constrains</span>
        </div>
        <div className="legend-item">
          <div className="legend-line" style={{ borderColor: '#ffd700' }}></div>
          <span>Validates</span>
        </div>
      </div>
      <div ref={containerRef} className="graph-container">
        <svg ref={svgRef}></svg>
      </div>
    </div>
  );
};

export default DependencyGraph;
