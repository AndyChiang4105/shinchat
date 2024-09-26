// Create scene
const scene = new THREE.Scene();

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 2);
scene.add(ambientLight);
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
directionalLight.position.set(0, 100, 0).normalize();
scene.add(directionalLight);

// Camera
const canvas = document.getElementById('model-canvas');
const camera = new THREE.PerspectiveCamera(75, canvas.width / canvas.height, 0.1, 10000);
camera.position.set(-135, -25, 932); // Update camera position to view the model from the front
camera.lookAt(new THREE.Vector3(0, 0, 0)); // Ensure camera points to the origin

// Renderer
const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true }); // Set alpha to true for transparent background
renderer.setSize(canvas.width, canvas.height);
renderer.setClearColor(0x000000, 0); // Set renderer background to transparent

// OrbitControls
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.maxDistance = 2000; // Set maximum distance
controls.minDistance = 10; // Set minimum distance

// Animation mixer and model variables
let mixer;
let currentModel;
const modelPaths = ['/static/models/Idle.fbx', '/static/models/think.fbx','/static/models/clapping.fbx','/static/models/correct.fbx','/static/models/sad.fbx','/static/models/wrong.fbx','/static/models/talk1.fbx','/static/models/talk2.fbx'];
let currentIndex = 0;

// Load model function
function loadModel(path) {
    if (currentModel) {
        scene.remove(currentModel);
    }

    const loader = new THREE.FBXLoader();
    loader.load(path, function(object) {
        object.scale.set(1.5, 1.5, 1.5); // Scale model
        object.position.set(0, -500, 0); // Center model at the origin

        currentModel = object;
        scene.add(currentModel);

        // Animation mixer
        mixer = new THREE.AnimationMixer(object);

        // Play all animations
        object.animations.forEach((clip) => {
            mixer.clipAction(clip).play();
        });
    });
}

// Initial model load
loadModel(modelPaths[currentIndex]);

// Animation loop
const clock = new THREE.Clock();
function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();
    if (mixer) mixer.update(delta);

    controls.update();
    renderer.render(scene, camera);
}

animate();

// Adjust camera and renderer size on window resize
function resize() {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    canvas.width = width; // Set canvas width to clientWidth
    canvas.height = height; // Set canvas height to clientHeight
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
}

window.addEventListener('resize', resize);
resize(); // Call to set initial size
