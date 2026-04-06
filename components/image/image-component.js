class ImageComponent extends HTMLElement {
  static get observedAttributes() {
    return ["tag", "source", "subtitle", "width"];
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
    const width = this.getAttribute("width") || "100%";

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          text-align: center;
          width: 100%;
        }

        .wrapper {
          display: block;
          width: 100%;
          text-align: center;
        }

        img {
          width: ${width};
          max-width: 100%;
          height: auto;
          display: block;
          margin: 0 auto;
          cursor: pointer;
          transition: opacity 0.15s;
        }

        img:hover {
          opacity: 0.85;
        }

        sub {
          font-size: 0.9rem;
          font-style: italic;
          display: block;
          margin-top: 4px;
          text-align: center;
        }

        .lightbox {
          display: none;
          position: fixed;
          top: 0; left: 0; right: 0; bottom: 0;
          background: rgba(0,0,0,0.85);
          z-index: 10000;
          justify-content: center;
          align-items: center;
          cursor: zoom-out;
        }

        .lightbox.open {
          display: flex;
        }

        .lightbox img {
          max-width: 92vw;
          max-height: 92vh;
          width: auto;
          object-fit: contain;
          border-radius: 6px;
          cursor: zoom-out;
        }
      </style>

      <div class="wrapper">
        <img id="${this.tag}" src="${this.source}" alt="${this.subtitle}">
        <sub>${this.subtitle}</sub>
      </div>

      <div class="lightbox">
        <img src="${this.source}" alt="${this.subtitle}">
      </div>
    `;

    const img = this.shadowRoot.querySelector('.wrapper img');
    const lightbox = this.shadowRoot.querySelector('.lightbox');

    img.addEventListener('click', () => lightbox.classList.add('open'));
    lightbox.addEventListener('click', () => lightbox.classList.remove('open'));
  }
}

customElements.define("image-component", ImageComponent);
