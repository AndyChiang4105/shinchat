// 創建場景
const scene = new THREE.Scene();

// 燈光
const ambientLight = new THREE.AmbientLight(0xffffff, 2);
scene.add(ambientLight);
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
directionalLight.position.set(0, 100, 0).normalize();
scene.add(directionalLight);

// 相機
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 10000); // 更新最大距離
camera.position.set(-135, -25, 932); // 更新相機位置，使其從正面看模型
camera.lookAt(new THREE.Vector3(0, 0, 0)); // 確保相機指向原點

// 渲染器
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true }); // 設置 alpha 為 true 以實現透明背景
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setClearColor(0x000000, 0); // 設置渲染器背景為透明
document.body.appendChild(renderer.domElement);

// OrbitControls
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.maxDistance = 2000; // 設定最大距離
controls.minDistance = 10; // 設定最小距離

// 動畫混合器和模型變量
let mixer;
let currentModel;
const modelPaths = ['/static/models/model.fbx', '/static/models/model2.fbx'];
let currentIndex = 0;

// 加載模型函數
function loadModel(path) {
    if (currentModel) {
        scene.remove(currentModel);
    }

    const loader = new THREE.FBXLoader();
    loader.load(path, function(object) {
        object.scale.set(1.5, 1.5, 1.5); // 縮小模型
        object.position.set(0, -500, 0); // 確保模型在原點

        currentModel = object;
        scene.add(currentModel);

        // 動畫混合器
        mixer = new THREE.AnimationMixer(object);

        // 播放所有動畫
        object.animations.forEach((clip) => {
            mixer.clipAction(clip).play();
        });
    });
}

// 初始加載模型
loadModel(modelPaths[currentIndex]);

// 定期切換模型的函數
function switchModel() {
    currentIndex = (currentIndex + 1) % modelPaths.length;// 將 currentIndex 增加 1，並用 modelPaths 的長度取模，確保 currentIndex 在 0 和 modelPaths.length - 1 之間循環
    loadModel(modelPaths[currentIndex]);// 根據 currentIndex 的值加載對應路徑的模型
}

// 每5秒切換一次模型
setInterval(switchModel, 5000);

// 動畫循環
const clock = new THREE.Clock();
function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();
    if (mixer) mixer.update(delta);

    controls.update();
    renderer.render(scene, camera);
}

animate();

// 當視窗大小改變時，相機和渲染器的大小也要改變
window.onresize = function() {
    const width = window.innerWidth;
    const height = window.innerHeight;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
};