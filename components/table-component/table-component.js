

class TableComponent extends HTMLElement {
  static get observedAttributes() {
    return ["subtitle"];
  }

  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback(name, _, newValue) {
    this[name] = newValue;
    if (this.isConnected) {
      this.render();
    }
  }

  render() {
    const subtitle = this.subtitle || "";
    this.shadowRoot.innerHTML = `
      <div class="table-shell">
        <slot></slot>
      </div>
      ${subtitle ? `<sub class="table-caption">${subtitle}</sub>` : ""}
      <style>
        :host {
          display: block;
          width: 100%;
          margin: 16px auto;
          text-align: center;
        }

        .table-shell {
          width: 100%;
          max-width: 1100px;
          margin: 0 auto;
          overflow-x: auto;
        }

        .table-caption {
          display: block;
          margin-top: 8px;
          font-size: 0.9rem;
          font-style: italic;
          color: #4b5563;
        }
      </style>
    `;
  }
}

customElements.define("table-component", TableComponent);
