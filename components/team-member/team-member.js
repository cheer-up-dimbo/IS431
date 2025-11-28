class TeamMember extends HTMLElement {
  static get observedAttributes() {
    return ["avatar", "name", "department", "year", "contribution"];
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
    this.render();
  }

  render() {
    this.shadowRoot.innerHTML = `
      <div>
        <img src="${this.avatar}" alt="${this.name}">
        <p><strong>${this.name}</strong></p>
        <p>${this.department}</p>
        <p>${this.year}</p>
        <p class="contribution">${this.contribution || ""}</p>

        <style>
          :host {
            display: block;
            max-width: 120px;
            text-align: center;
          }

          img {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            display: block;
            margin: auto;
            object-fit: contain;      /* prevents stretching */
            object-position: center; /* centers the image */
          }

          p {
            text-align: center;
            margin: 8px 0;
          }

          .contribution {
            font-size: 12px;      
            text-align: justify;  
            margin: 4px 0 0 0;
          }

          @media (max-width: 599px) {
            img {
              display: none;
            }
          }
        </style>
      </div>
    `;
  }
}

customElements.define("team-member", TeamMember);
