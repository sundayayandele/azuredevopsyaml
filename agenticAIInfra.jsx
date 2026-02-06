import { useState } from "react";

const COLORS = {
  bg: "#0a0e17",
  surface: "#111827",
  surfaceAlt: "#1a2235",
  border: "#1e293b",
  borderActive: "#3b82f6",
  text: "#e2e8f0",
  textMuted: "#94a3b8",
  textDim: "#64748b",
  accent: "#3b82f6",
  accentGlow: "rgba(59,130,246,0.15)",
  inspection: { bg: "#7c3aed", light: "#a78bfa", glow: "rgba(124,58,237,0.2)" },
  severity: { bg: "#f59e0b", light: "#fbbf24", glow: "rgba(245,158,11,0.2)" },
  planning: { bg: "#10b981", light: "#34d399", glow: "rgba(16,185,129,0.2)" },
  cost: { bg: "#06b6d4", light: "#22d3ee", glow: "rgba(6,182,212,0.2)" },
  orchestrator: { bg: "#ec4899", light: "#f472b6", glow: "rgba(236,72,153,0.2)" },
  success: "#10b981",
  warning: "#f59e0b",
  danger: "#ef4444",
};

const tabs = [
  { id: "overview", label: "System Overview" },
  { id: "agents", label: "Agent Deep-Dive" },
  { id: "dataflow", label: "Data Pipeline" },
  { id: "rag", label: "RAG Architecture" },
  { id: "deploy", label: "Deployment" },
  { id: "tech", label: "Tech Stack" },
];

const agentData = [
  {
    id: "inspection",
    name: "Inspection Agent",
    icon: "🛩️",
    color: COLORS.inspection,
    subtitle: "Computer Vision & Drone Integration",
    description: "Processes drone/sensor imagery using advanced computer vision models (YOLOv8, CNNs) to detect structural anomalies — cracks, corrosion, deformation, vegetation overgrowth.",
    inputs: ["Drone 4K imagery", "IoT sensor telemetry", "LIDAR point clouds", "Thermal imaging data"],
    outputs: ["Annotated defect images", "Geo-tagged anomaly reports", "3D scene graphs", "Confidence scores"],
    models: ["YOLOv8 (Object Detection)", "SegFormer (Semantic Segmentation)", "ResNet-50 (Classification)", "3D Scene Graph Generator"],
    tools: ["OpenCV", "SLAM Navigation", "DJI SDK", "Edge Inference (Jetson)"],
    metrics: [
      { label: "Detection Accuracy", value: "96.2%", status: "success" },
      { label: "Processing Latency", value: "<2.1s", status: "success" },
      { label: "False Positive Rate", value: "3.8%", status: "warning" },
      { label: "Coverage per Flight", value: "85%", status: "success" },
    ],
  },
  {
    id: "severity",
    name: "Severity Classification Agent",
    icon: "🔍",
    color: COLORS.severity,
    subtitle: "Risk Assessment & Urgency Triage",
    description: "Determines urgency and risk classification (cosmetic vs. critical) using multi-modal analysis combining visual defect data with structural engineering knowledge bases.",
    inputs: ["Defect annotations", "Historical severity data", "Structural load models", "Weather/environmental context"],
    outputs: ["Severity score (1-10)", "Risk classification", "Urgency priority queue", "Safety compliance flags"],
    models: ["LLM Classifier (Claude/GPT)", "Random Forest (Severity)", "Bayesian Risk Network", "Time-Series Degradation Model"],
    tools: ["Structural Analysis APIs", "Risk Matrix Engine", "Compliance Checker", "Alert Notification Service"],
    metrics: [
      { label: "Classification Accuracy", value: "94.7%", status: "success" },
      { label: "Critical Miss Rate", value: "0.3%", status: "success" },
      { label: "Avg Triage Time", value: "4.2s", status: "success" },
      { label: "Inter-rater Agreement", value: "κ=0.89", status: "success" },
    ],
  },
  {
    id: "planning",
    name: "Maintenance Planning Agent",
    icon: "📋",
    color: COLORS.planning,
    subtitle: "RAG-Powered Prescriptive Planning",
    description: "RAG system with historical repair data that generates actionable maintenance plans by synthesizing maintenance manuals, past repair records, and domain expertise via retrieval-augmented generation.",
    inputs: ["Severity reports", "Maintenance manuals (vectorized)", "Historical repair records", "Parts inventory status"],
    outputs: ["Maintenance work orders", "Step-by-step repair procedures", "Parts/materials requisitions", "Timeline estimates"],
    models: ["Claude Sonnet 4.5 (RAG Reasoning)", "BGE-M3 Embeddings", "Cross-Encoder Re-ranker", "Task Decomposition Planner"],
    tools: ["ChromaDB Vector Store", "Document Chunker", "CMMS API Integration", "Knowledge Graph (Neo4j)"],
    metrics: [
      { label: "Plan Relevance", value: "92.1%", status: "success" },
      { label: "Manual Coverage", value: "15K+ docs", status: "success" },
      { label: "Retrieval Precision", value: "91.3%", status: "success" },
      { label: "Avg Plan Gen", value: "8.5s", status: "warning" },
    ],
  },
  {
    id: "cost",
    name: "Cost Optimization Agent",
    icon: "💰",
    color: COLORS.cost,
    subtitle: "Schedule & Budget Optimization",
    description: "Schedules repairs to minimize disruption and optimize budget allocation using constraint satisfaction, linear programming, and predictive cost modeling across the asset portfolio.",
    inputs: ["Maintenance plans", "Budget constraints", "Crew availability", "Asset criticality ratings"],
    outputs: ["Optimized repair schedule", "Budget allocation plan", "Resource deployment map", "ROI projections"],
    models: ["OR-Tools (Constraint Solver)", "Monte Carlo Cost Simulation", "Reinforcement Learning Scheduler", "Demand Forecast (Prophet)"],
    tools: ["Google OR-Tools", "Gurobi Optimizer", "Calendar API", "ERP Integration (SAP/Oracle)"],
    metrics: [
      { label: "Cost Reduction", value: "32%", status: "success" },
      { label: "Downtime Reduction", value: "47%", status: "success" },
      { label: "Schedule Adherence", value: "91%", status: "success" },
      { label: "Budget Accuracy", value: "±8%", status: "warning" },
    ],
  },
];

function MetricBadge({ label, value, status }) {
  const statusColors = { success: COLORS.success, warning: COLORS.warning, danger: COLORS.danger };
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 12px", background: "rgba(255,255,255,0.03)", borderRadius: 8, borderLeft: `3px solid ${statusColors[status]}` }}>
      <span style={{ color: COLORS.textMuted, fontSize: 12 }}>{label}</span>
      <span style={{ color: statusColors[status], fontWeight: 700, fontSize: 14, fontFamily: "'JetBrains Mono', monospace" }}>{value}</span>
    </div>
  );
}

function AgentCard({ agent, expanded, onToggle }) {
  return (
    <div
      onClick={onToggle}
      style={{
        background: expanded ? COLORS.surfaceAlt : COLORS.surface,
        border: `1px solid ${expanded ? agent.color.bg : COLORS.border}`,
        borderRadius: 16,
        padding: expanded ? 28 : 20,
        cursor: "pointer",
        transition: "all 0.3s ease",
        boxShadow: expanded ? `0 0 30px ${agent.color.glow}` : "none",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: expanded ? 20 : 0 }}>
        <div style={{ fontSize: 32, width: 52, height: 52, display: "flex", alignItems: "center", justifyContent: "center", background: agent.color.glow, borderRadius: 14 }}>
          {agent.icon}
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ color: COLORS.text, fontWeight: 700, fontSize: 17 }}>{agent.name}</div>
          <div style={{ color: agent.color.light, fontSize: 12, fontWeight: 500, letterSpacing: 0.5 }}>{agent.subtitle}</div>
        </div>
        <div style={{ color: COLORS.textDim, fontSize: 20, transform: expanded ? "rotate(180deg)" : "rotate(0)", transition: "transform 0.3s" }}>▾</div>
      </div>

      {expanded && (
        <div style={{ marginTop: 8 }}>
          <p style={{ color: COLORS.textMuted, fontSize: 14, lineHeight: 1.7, marginBottom: 24 }}>{agent.description}</p>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 24 }}>
            <div>
              <div style={{ color: COLORS.text, fontWeight: 600, fontSize: 13, marginBottom: 10, textTransform: "uppercase", letterSpacing: 1 }}>⬇ Inputs</div>
              {agent.inputs.map((i, idx) => (
                <div key={idx} style={{ color: COLORS.textMuted, fontSize: 13, padding: "5px 0", borderBottom: `1px solid ${COLORS.border}` }}>• {i}</div>
              ))}
            </div>
            <div>
              <div style={{ color: COLORS.text, fontWeight: 600, fontSize: 13, marginBottom: 10, textTransform: "uppercase", letterSpacing: 1 }}>⬆ Outputs</div>
              {agent.outputs.map((o, idx) => (
                <div key={idx} style={{ color: COLORS.textMuted, fontSize: 13, padding: "5px 0", borderBottom: `1px solid ${COLORS.border}` }}>• {o}</div>
              ))}
            </div>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 24 }}>
            <div>
              <div style={{ color: COLORS.text, fontWeight: 600, fontSize: 13, marginBottom: 10, textTransform: "uppercase", letterSpacing: 1 }}>🧠 Models</div>
              {agent.models.map((m, idx) => (
                <div key={idx} style={{ display: "inline-block", background: agent.color.glow, color: agent.color.light, fontSize: 11, padding: "4px 10px", borderRadius: 20, margin: "3px 4px 3px 0", fontWeight: 500 }}>{m}</div>
              ))}
            </div>
            <div>
              <div style={{ color: COLORS.text, fontWeight: 600, fontSize: 13, marginBottom: 10, textTransform: "uppercase", letterSpacing: 1 }}>🔧 Tools</div>
              {agent.tools.map((t, idx) => (
                <div key={idx} style={{ display: "inline-block", background: "rgba(255,255,255,0.05)", color: COLORS.textMuted, fontSize: 11, padding: "4px 10px", borderRadius: 20, margin: "3px 4px 3px 0", fontWeight: 500 }}>{t}</div>
              ))}
            </div>
          </div>

          <div style={{ color: COLORS.text, fontWeight: 600, fontSize: 13, marginBottom: 10, textTransform: "uppercase", letterSpacing: 1 }}>📊 Performance Metrics</div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
            {agent.metrics.map((m, idx) => <MetricBadge key={idx} {...m} />)}
          </div>
        </div>
      )}
    </div>
  );
}

function OverviewTab() {
  return (
    <div>
      <div style={{ textAlign: "center", marginBottom: 40 }}>
        <h2 style={{ color: COLORS.text, fontSize: 26, fontWeight: 800, margin: 0, letterSpacing: -0.5 }}>Multi-Agent System Architecture</h2>
        <p style={{ color: COLORS.textMuted, fontSize: 14, marginTop: 8 }}>Infrastructure AI Agents for Predictive Maintenance & Optimization</p>
      </div>

      {/* Orchestrator */}
      <div style={{ background: `linear-gradient(135deg, ${COLORS.orchestrator.glow}, transparent)`, border: `1px solid ${COLORS.orchestrator.bg}`, borderRadius: 16, padding: 24, marginBottom: 20, textAlign: "center" }}>
        <div style={{ fontSize: 14, color: COLORS.orchestrator.light, fontWeight: 700, textTransform: "uppercase", letterSpacing: 2, marginBottom: 6 }}>🎛️ Orchestration Layer</div>
        <div style={{ color: COLORS.textMuted, fontSize: 13 }}>LangGraph / CrewAI Workflow Engine • Human-in-the-Loop Gate • MCP Protocol • State Machine</div>
      </div>

      {/* Agent Pipeline */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: 20 }}>
        {agentData.map((agent, idx) => (
          <div key={agent.id}>
            <div style={{
              background: COLORS.surface,
              border: `1px solid ${COLORS.border}`,
              borderTop: `3px solid ${agent.color.bg}`,
              borderRadius: 14,
              padding: 20,
              textAlign: "center",
              minHeight: 180,
            }}>
              <div style={{ fontSize: 36, marginBottom: 10 }}>{agent.icon}</div>
              <div style={{ color: COLORS.text, fontWeight: 700, fontSize: 14, marginBottom: 6 }}>{agent.name}</div>
              <div style={{ color: agent.color.light, fontSize: 11, fontWeight: 500, marginBottom: 10 }}>{agent.subtitle}</div>
              <div style={{ color: COLORS.textDim, fontSize: 11, lineHeight: 1.6 }}>
                {agent.description.split('.')[0]}.
              </div>
            </div>
            {idx < 3 && (
              <div style={{ textAlign: "center", padding: "8px 0", color: COLORS.accent, fontSize: 22, fontWeight: 700 }}>→</div>
            )}
          </div>
        ))}
      </div>

      {/* Flow Summary */}
      <div style={{ background: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: 14, padding: 24 }}>
        <div style={{ color: COLORS.text, fontWeight: 700, fontSize: 15, marginBottom: 16 }}>Overall Flow & Benefit</div>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8, flexWrap: "wrap" }}>
          {[
            { label: "Drone Flight", color: COLORS.inspection.bg },
            { label: "Image Capture", color: COLORS.inspection.bg },
            { label: "Defect Detection", color: COLORS.inspection.bg },
            { label: "Severity Triage", color: COLORS.severity.bg },
            { label: "RAG Planning", color: COLORS.planning.bg },
            { label: "Cost Optimization", color: COLORS.cost.bg },
            { label: "Repair Schedule", color: COLORS.accent },
          ].map((step, idx, arr) => (
            <div key={idx} style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <div style={{
                background: step.color,
                color: "#fff",
                fontSize: 11,
                fontWeight: 600,
                padding: "6px 14px",
                borderRadius: 20,
              }}>{step.label}</div>
              {idx < arr.length - 1 && <span style={{ color: COLORS.textDim, fontSize: 16 }}>→</span>}
            </div>
          ))}
        </div>
      </div>

      {/* Key Architecture Decisions */}
      <div style={{ marginTop: 24, display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 14 }}>
        {[
          { title: "Sequential Pipeline", desc: "Agents process in order: Inspection → Severity → Planning → Cost. Each agent's output feeds the next, ensuring data integrity and traceable decision chains.", icon: "🔗" },
          { title: "Human-in-the-Loop", desc: "Critical severity classifications (≥8/10) require human approval before maintenance plans are generated. Prevents autonomous high-cost decisions.", icon: "👤" },
          { title: "Event-Driven Async", desc: "Agents communicate via message queues (Kafka/RabbitMQ). Enables parallel processing of multiple inspection batches and fault-tolerant retry logic.", icon: "⚡" },
        ].map((item, idx) => (
          <div key={idx} style={{ background: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: 14, padding: 20 }}>
            <div style={{ fontSize: 28, marginBottom: 10 }}>{item.icon}</div>
            <div style={{ color: COLORS.text, fontWeight: 700, fontSize: 14, marginBottom: 8 }}>{item.title}</div>
            <div style={{ color: COLORS.textMuted, fontSize: 12, lineHeight: 1.7 }}>{item.desc}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function AgentsTab() {
  const [expanded, setExpanded] = useState("inspection");
  return (
    <div>
      <div style={{ marginBottom: 28 }}>
        <h2 style={{ color: COLORS.text, fontSize: 24, fontWeight: 800, margin: 0 }}>Agent Deep-Dive</h2>
        <p style={{ color: COLORS.textMuted, fontSize: 13, marginTop: 6 }}>Click any agent to explore its models, tools, I/O specifications, and performance metrics</p>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
        {agentData.map(agent => (
          <AgentCard
            key={agent.id}
            agent={agent}
            expanded={expanded === agent.id}
            onToggle={() => setExpanded(expanded === agent.id ? null : agent.id)}
          />
        ))}
      </div>
    </div>
  );
}

function DataFlowTab() {
  const layers = [
    {
      name: "DATA INGESTION LAYER",
      color: COLORS.inspection.bg,
      items: [
        { name: "Drone Fleet", desc: "DJI Matrice 350 RTK • 4K cameras • LIDAR • Thermal sensors", icon: "🛩️" },
        { name: "IoT Sensors", desc: "Vibration, temperature, humidity, strain gauges via MQTT", icon: "📡" },
        { name: "Satellite Imagery", desc: "Periodic wide-area monitoring for macro-level changes", icon: "🛰️" },
        { name: "Manual Reports", desc: "Technician field reports, historical inspection logs", icon: "📝" },
      ],
    },
    {
      name: "DATA PROCESSING LAYER",
      color: COLORS.severity.bg,
      items: [
        { name: "Stream Processing", desc: "Apache Kafka → Flink for real-time telemetry ingestion", icon: "🌊" },
        { name: "Image Pipeline", desc: "Pre-processing (denoise, normalize, resize) → GPU inference queue", icon: "🖼️" },
        { name: "Feature Store", desc: "Feast — serving computed features (degradation rate, defect density)", icon: "📦" },
        { name: "Data Lake", desc: "MinIO / S3 — raw imagery, sensor dumps, and processed datasets", icon: "🗄️" },
      ],
    },
    {
      name: "AI / ML INFERENCE LAYER",
      color: COLORS.planning.bg,
      items: [
        { name: "Vision Models", desc: "YOLOv8 + SegFormer on NVIDIA Triton Inference Server", icon: "👁️" },
        { name: "LLM Gateway", desc: "Claude API / vLLM self-hosted for severity reasoning & planning", icon: "🧠" },
        { name: "RAG Engine", desc: "ChromaDB + BGE-M3 embeddings + cross-encoder re-ranking", icon: "🔍" },
        { name: "Optimization Solver", desc: "Google OR-Tools / Gurobi for constraint-based scheduling", icon: "⚙️" },
      ],
    },
    {
      name: "APPLICATION & OUTPUT LAYER",
      color: COLORS.cost.bg,
      items: [
        { name: "Dashboard", desc: "Real-time map view, defect gallery, KPI cards, trend charts", icon: "📊" },
        { name: "Work Order System", desc: "Auto-generated work orders → CMMS (SAP PM / IBM Maximo)", icon: "📋" },
        { name: "Alert Engine", desc: "Priority-based notifications via Slack, email, SMS, PagerDuty", icon: "🔔" },
        { name: "Reporting", desc: "Automated compliance reports, audit trails, executive summaries", icon: "📄" },
      ],
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 28 }}>
        <h2 style={{ color: COLORS.text, fontSize: 24, fontWeight: 800, margin: 0 }}>Data Pipeline Architecture</h2>
        <p style={{ color: COLORS.textMuted, fontSize: 13, marginTop: 6 }}>End-to-end data flow from ingestion to actionable outputs</p>
      </div>

      {layers.map((layer, idx) => (
        <div key={idx} style={{ marginBottom: idx < layers.length - 1 ? 8 : 0 }}>
          <div style={{
            background: `linear-gradient(90deg, ${layer.color}22, transparent)`,
            borderLeft: `4px solid ${layer.color}`,
            borderRadius: "0 12px 12px 0",
            padding: "12px 20px",
            marginBottom: 12,
          }}>
            <span style={{ color: layer.color, fontWeight: 800, fontSize: 12, letterSpacing: 2 }}>{layer.name}</span>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10, paddingLeft: 20, marginBottom: 16 }}>
            {layer.items.map((item, i) => (
              <div key={i} style={{ background: COLORS.surface, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: 16 }}>
                <div style={{ fontSize: 24, marginBottom: 8 }}>{item.icon}</div>
                <div style={{ color: COLORS.text, fontWeight: 700, fontSize: 13, marginBottom: 4 }}>{item.name}</div>
                <div style={{ color: COLORS.textDim, fontSize: 11, lineHeight: 1.6 }}>{item.desc}</div>
              </div>
            ))}
          </div>
          {idx < layers.length - 1 && (
            <div style={{ textAlign: "center", color: COLORS.textDim, fontSize: 18, margin: "4px 0" }}>▼</div>
          )}
        </div>
      ))}
    </div>
  );
}

function RAGTab() {
  return (
    <div>
 