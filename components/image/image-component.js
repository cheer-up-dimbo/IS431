// class ImageComponent extends HTMLElement {
//   static get observedAttributes() {
//     return ["tag", "source", "subtitle"];
//   }

//   constructor() {
//     super();
//     this.attachShadow({ mode: "open" });
//   }

//   connectedCallback() {
//     this.render();
//   }

//   attributeChangedCallback(name, _, newValue) {
//     this[name] = newValue;
//   }

//   render() {
//     const div = document.createElement("div");
//     div.innerHTML = `
//     <img id="${this.tag}" src="${this.source}" alt="${this.subtitle}">
//     <sub>${this.subtitle}</sub>
//     <style>
//       :host {
//         display: block;
//         text-align: center;
//       }

//       img {
//         width: 100%;
//       }

//       sub {
//         font-size: 1rem;
//         font-style: italic;
//       }
//     </style>
//   `;

//     this.shadowRoot.appendChild(div);
//   }
// }

// customElements.define("image-component", ImageComponent);

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
          display: block;        /* FIX: wrapper now full width */
          width: 100%;
          text-align: center;
        }

        img {
          width: ${width};       /* custom width */
          max-width: 100%;       /* ensures it never exceeds container */
          height: auto;
          display: block;
          margin: 0 auto;
        }

        sub {
          font-size: 0.9rem;
          font-style: italic;
          display: block;
          margin-top: 4px;
          text-align: center;
        }
      </style>

      <div class="wrapper">
        <img id="${this.tag}" src="${this.source}" alt="${this.subtitle}">
        <sub>${this.subtitle}</sub>
      </div>
    `;
  }
}

customElements.define("image-component", ImageComponent);
