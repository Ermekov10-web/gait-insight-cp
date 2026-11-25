# NEUROMOTION_PRO_V1
from pathlib import Path
import base64
import json
from zipfile import ZipFile

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "research"
MODEL = ROOT / "assets" / "neuro_male.glb"
MODEL_ARCHIVE = ROOT / "neuro_model_for_presentation.zip"


def read_model():
    if MODEL.is_file():
        return MODEL.read_bytes()
    if MODEL_ARCHIVE.is_file():
        with ZipFile(MODEL_ARCHIVE) as archive:
            return archive.read("assets/neuro_male.glb")
    return b""

CONDITIONS = ["Baseline", "Verbal", "VR"]

JOINTS = {
    "pelvis": "aSagP",
    "hip": "aSagH",
    "knee": "aSagK",
    "ankle": "aSagA"
}


@st.cache_data(show_spinner=False)
def load_data():

    motion = {}
    scores = {}

    for condition in CONDITIONS:

        for prefix, target in [
            ("Kinematics_Kinetics", motion),
            ("Discrete_Parameters", scores)
        ]:

            path = DATA / f"{prefix}_{condition}.csv"

            if not path.exists():
                continue

            df = pd.read_csv(
                path,
                sep=";",
                decimal=",",
                encoding="utf-8-sig"
            )

            df.columns = df.columns.str.strip()

            df["subject"] = df["subject"].astype(str)
            df["side"] = df["side"].astype(str).str.upper()

            target[condition] = df

    return motion, scores


def get_curves(df, subject, side):

    selected = df[
        (df["subject"] == subject)
        & (df["side"] == side)
    ]

    if selected.empty:
        return None

    result = {}

    for name, prefix in JOINTS.items():

        columns = [
            f"{prefix}_pct_GC_{i}"
            for i in range(0, 1001, 20)
        ]

        if not set(columns).issubset(selected.columns):
            return None

        values = (
            selected[columns]
            .apply(pd.to_numeric, errors="coerce")
            .mean()
            .to_numpy(dtype=float)
        )

        if not np.isfinite(values).all():
            return None

        result[name] = np.interp(
            np.linspace(0, 100, 101),
            np.linspace(0, 100, 51),
            values
        ).round(3).tolist()

    return result


def get_scores(df, subject, side):

    if df is None:
        return {}

    selected = df[
        (df["subject"] == subject)
        & (df["side"] == side)
    ]

    result = {}

    for column in [
        "GPS_a",
        "GVS_aSagH",
        "GVS_aSagK",
        "GVS_aSagA",
        "GVS_aSagP"
    ]:

        if column not in selected:
            continue

        value = pd.to_numeric(
            selected[column],
            errors="coerce"
        ).mean()

        if np.isfinite(value):
            result[column] = round(float(value), 2)

    return result


HTML = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">

<style>

* {
    box-sizing:border-box;
}

body {
    margin:0;
    font-family:Arial,sans-serif;
    color:#c9ffe5;
    background:#021009;
}

.hud {
    position:relative;
    overflow:hidden;
    border:1px solid #197549;
    border-radius:15px;

    background:
        radial-gradient(
            ellipse at 50% 45%,
            #084628 0%,
            #031e11 45%,
            #020e08 80%
        );
}

.header {
    padding:20px;
    border-bottom:1px solid #155737;
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.brand {
    color:#35ff9e;
    font-size:10px;
    letter-spacing:4px;
}

h1 {
    font-size:26px;
    margin:7px 0;
    color:#e2faff;
    font-weight:500;
}

.subtitle {
    font-size:11px;
    color:#80bfa1;
    line-height:1.6;
}

.live {
    padding:8px 12px;
    border:1px solid #1e975d;
    background:#083b23;
    font-size:10px;
    color:#65ffb5;
    border-radius:4px;
}

.main {
    display:grid;
    grid-template-columns:170px 1fr 170px;
    gap:9px;
    padding:12px;
}

.side {
    display:flex;
    flex-direction:column;
    gap:12px;
}

.card {
    position:relative;
    padding:13px;
    border:1px solid #166d43;
    background:rgba(4,22,35,.83);
    box-shadow:inset 0 0 24px #0a4428;
}

.card:before {
    content:"";
    position:absolute;
    width:19px;
    height:19px;
    top:-1px;
    left:-1px;
    border-top:2px solid #3dffa2;
    border-left:2px solid #3dffa2;
}

.label {
    color:#66e8aa;
    letter-spacing:1px;
    font-size:10px;
    text-transform:uppercase;
}

.value {
    font-family:monospace;
    font-size:26px;
    margin:10px 0;
    color:#85ffc4;
    text-shadow:0 0 15px #1cff92;
}

.small {
    color:#90cbaf;
    font-size:10px;
    line-height:1.7;
}

.circle {
    width:105px;
    height:105px;
    margin:14px auto;
    border-radius:50%;
    border:2px solid #26a065;
    outline:1px dashed #3db97d;
    outline-offset:5px;

    display:flex;
    align-items:center;
    justify-content:center;

    background:
        repeating-radial-gradient(
            circle,
            transparent 0px,
            transparent 9px,
            #125d39 10px,
            transparent 11px
        );

    box-shadow:
        0 0 20px #0b6c9b66,
        inset 0 0 18px #0c7ab066;
}

.circle span {
    color:#b6ffdc;
    font-family:monospace;
    font-size:21px;
    text-shadow:0 0 12px cyan;
}

.stage {
    position:relative;
    min-width:0;
    height:660px;
    overflow:hidden;

    background-image:
        linear-gradient(#17557322 1px,transparent 1px),
        linear-gradient(90deg,#17557322 1px,transparent 1px);

    background-size:30px 30px;
    border:1px solid #165c3a;
}

.stage canvas {
    display:block;
}

.stage-title {
    position:absolute;
    top:12px;
    width:100%;
    text-align:center;
    color:#71e6ae;
    font-size:10px;
    letter-spacing:2px;
    pointer-events:none;
    z-index:3;
}

.stage-bottom {
    position:absolute;
    bottom:12px;
    width:100%;
    text-align:center;
    font-size:10px;
    color:#91d0b2;
    pointer-events:none;
}

.cross {
    position:absolute;
    top:50%;
    left:50%;
    width:100%;
    border-top:1px dashed #2784a94a;
    transform:translate(-50%,-50%);
    pointer-events:none;
}

.controls {
    display:flex;
    gap:7px;
    flex-wrap:wrap;
    padding:12px;
    border-top:1px solid #17603d;
}

button,select {
    cursor:pointer;
    background:#094026;
    color:#a9ffd6;
    border:1px solid #228b59;
    padding:10px 13px;
    font-size:11px;
    border-radius:4px;
}

button:hover,button.active {
    background:#14ae64;
    color:white;
    box-shadow:0 0 12px #19a9e444;
}

.timeline {
    padding:10px 20px;
}

input[type=range] {
    width:100%;
    accent-color:#48ffa7;
}

.graph-box {
    margin:12px;
    border:1px solid #1e734a;
    background:#042013;
    padding:15px;
}

#graph {
    width:100%;
    height:165px;
    display:block;
}

#loading {
    position:absolute;
    top:45%;
    left:10%;
    right:10%;
    text-align:center;
    color:#8effc9;
    font-size:12px;
    line-height:1.6;
}

.legend {
    display:flex;
    gap:16px;
    font-size:11px;
    margin:12px 0;
}

@media(max-width:780px) {

    .main {
        grid-template-columns:1fr 1fr;
    }

    .stage {
        grid-column:1/3;
        grid-row:1;
        height:540px;
    }

    .side {
        grid-row:2;
    }
}

</style>

<script type="importmap">
{
    "imports":{
        "three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
        "three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"
    }
}
</script>

</head>
<body>

<div class="hud">

    <div class="header">
        <div>
            <div class="brand">
                NEUROKINETICS / BIOMECHANICAL LAB
            </div>
            <h1>NeuroMotion PRO</h1>
            <div class="subtitle">
                Интерактивный биомеханический профиль
            </div>
        </div>

        <div class="live">
            ● ● НАУЧНЫЕ ДАННЫЕ
        </div>
    </div>

    <div class="main">

        <div class="side">

            <div class="card">

                <div class="label">Участник</div>
                <div class="value" id="subject"
                     style="font-size:17px">—</div>

                <div class="small" id="side"></div>

            </div>

            <div class="card">

                <div class="label">Цикл ходьбы</div>

                <div class="circle">
                    <span id="phaseCircle">0%</span>
                </div>

                <div class="small">
                    Нормализованная фаза движения
                </div>

            </div>

            <div class="card">

                
    <div class="label">Угол таза</div>
    <div class="value" id="pelvisValue">—</div>

    <div class="label">Тазобедренный сустав</div>
    
                <div class="value" id="hipValue">—</div>

            </div>

            <div class="card">

                <div class="label">Коленный сустав</div>
                <div class="value" id="kneeValue">—</div>

            </div>

        </div>

        <div class="stage" id="stage">

            <div class="stage-title">
                HUMAN MOTION / 3D VISUALIZATION
            </div>

            <div class="cross"></div>

            <div id="loading">
                Загрузка трёхмерной модели...
            </div>

            <div class="stage-bottom">
                Вращение мышью · Приближение · Выбор сустава
            </div>

        </div>

        <div class="side">

            <div class="card">

                <div class="label">GPS — Gait Profile Score</div>

                <div class="circle">
                    <span id="gps">—</span>
                </div>

                <div class="small">
                    Показатель отклонения походки
                    от нормативного профиля
                </div>

            </div>

            <div class="card">

                <div class="label">GVS выбранного сустава</div>

                <div class="value" id="gvs">—</div>

                <div class="small" id="jointLabel">
                    Коленный сустав
                </div>

            </div>

            <div class="card">

                <div class="label">Голеностопный сустав</div>

                <div class="value" id="ankleValue">—</div>

            </div>

            <div class="card">

                <div class="label">Различие условий</div>

                <div class="value" id="difference">—</div>

                <div class="small">
                    Угловая разница в текущей фазе
                </div>

            </div>

        </div>

    </div>

    <div class="controls">

        <button id="play">▶ Движение</button>

        <button id="front">Спереди</button>

        <button id="sideView">Сбоку</button>

        <button id="rotate">360°</button>

        
    <button class="joint" data-joint="pelvis">
        Таз
    </button>

    <button class="joint" data-joint="hip">
        Тазобедренный
    </button>
    

        <button class="joint active" data-joint="knee">
            Колено
        </button>

        <button class="joint" data-joint="ankle">
            Голеностоп
        </button>

        <select id="condition"></select>

        <select id="speed">
            <option value="0.5">0.5×</option>
            <option value="1" selected>1×</option>
            <option value="2">2×</option>
        </select>

    </div>

    
    <div class="graph-box">

        <div class="label">
            NEUROVOICE · ГОЛОСОВОЙ ПОМОЩНИК
        </div>

        <p class="small">
            Скажите: «Покажи колено»,
            «Объясни GPS», «Включи движение»
            или «Пауза».
        </p>

        <div class="controls">

            <button id="speakData">
                🔊 Озвучить показатели
            </button>

            <button id="listen">
                🎙 Голосовая команда
            </button>

            <button id="stopVoice">
                Остановить голос
            </button>

        </div>

        <input id="voiceText"
            placeholder="Или напишите команду..."
            style="
                width:75%;
                padding:12px;
                background:#071e15;
                color:#ddffee;
                border:1px solid #357653;
                border-radius:5px;
            ">

        <button id="sendVoice">
            Выполнить
        </button>

        <p id="voiceStatus" class="small">
            Помощник готов.
        </p>

        <p class="small">
            Используйте только демонстрационные данные.
            Распознавание речи зависит от браузера
            и может использовать интернет-сервис.
        </p>

    </div>

    <div class="timeline">
    

        <div class="subtitle" id="phaseText">
            Цикл ходьбы: 0%
        </div>

        <input id="phase" type="range"
               min="0" max="100" value="0" step=".1">

    </div>

    <div class="graph-box">

        <div class="label" id="graphTitle">
            СРАВНЕНИЕ СУСТАВНЫХ УГЛОВ
        </div>

        <div class="legend" id="legend"></div>

        <canvas id="graph"></canvas>

        <div class="small">
            Измерения из исследования KU Leuven.
            Линии отображают усреднённые циклы одного участника.
            Различия не являются диагнозом.
        </div>

    </div>

</div>


<script type="module">

import * as THREE from "three";

import { OrbitControls }
from "three/addons/controls/OrbitControls.js";

import { GLTFLoader }
from "three/addons/loaders/GLTFLoader.js";

import { EffectComposer }
from "three/addons/postprocessing/EffectComposer.js";

import { RenderPass }
from "three/addons/postprocessing/RenderPass.js";

import { UnrealBloomPass }
from "three/addons/postprocessing/UnrealBloomPass.js";


const DATA = __PAYLOAD__;

const ASSET = "__MODEL_BASE64__";

const $ = id => document.getElementById(id);

const stage = $("stage");

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
    34,
    stage.clientWidth/stage.clientHeight,
    .01,
    100
);

camera.position.set(0,1.1,3.9);

const renderer = new THREE.WebGLRenderer({
    antialias:true,
    alpha:true
});

renderer.setPixelRatio(
    Math.min(devicePixelRatio,1.5)
);

renderer.setSize(
    stage.clientWidth,
    stage.clientHeight
);

renderer.setClearColor(0x021009,0);

renderer.toneMapping=THREE.ACESFilmicToneMapping;

renderer.toneMappingExposure=1.25;

stage.appendChild(renderer.domElement);


const composer = new EffectComposer(renderer);

composer.addPass(
    new RenderPass(scene,camera)
);

const bloom = new UnrealBloomPass(
    new THREE.Vector2(
        stage.clientWidth,
        stage.clientHeight
    ),
    .85,
    .35,
    .65
);

composer.addPass(bloom);


const orbit = new OrbitControls(
    camera,renderer.domElement
);

orbit.target.set(0,.91,0);

orbit.enableDamping=true;

orbit.minDistance=1.8;
orbit.maxDistance=7;

orbit.update();


scene.add(
    new THREE.HemisphereLight(
        0xa4ffd3,0x03301a,2.2
    )
);

function light(color,power,x,y,z){

    const l=new THREE.DirectionalLight(color,power);

    l.position.set(x,y,z);

    scene.add(l);
}

light(0x6cffb8,4,1,3,3);
light(0x15ff8f,3,-3,1,-2);
light(0xa7ffd5,2,3,2,-3);


// Holographic material

const bodyMaterial=new THREE.MeshStandardMaterial({

    color:0x077942,

    metalness:.45,

    roughness:.25,

    emissive:0x037840,

    emissiveIntensity:.65

});

bodyMaterial.onBeforeCompile=shader=>{

    shader.fragmentShader=shader.fragmentShader.replace(

        "#include <dithering_fragment>",

        `
        float edge = pow(
            1.0 - abs(dot(
                normalize(normal),
                normalize(vViewPosition)
            )),
            2.0
        );

        float scan =
            0.5 + 0.5*sin(gl_FragCoord.y*0.85);

        gl_FragColor.rgb +=
            vec3(0.03,0.95,0.45)
            * edge * 0.85;

        gl_FragColor.rgb +=
            vec3(0.0,0.09,0.045)
            * scan;

        #include <dithering_fragment>
        `
    );
};


const wireMaterial=new THREE.MeshBasicMaterial({

    color:0x44ffa5,

    wireframe:true,

    transparent:true,

    opacity:.28,

    depthWrite:false,

    polygonOffset:true,

    polygonOffsetFactor:-1,

    polygonOffsetUnits:-1

});


const root=new THREE.Group();

scene.add(root);


// Glowing platform

for(let i=0;i<5;i++){

    const ring=new THREE.Mesh(

        new THREE.TorusGeometry(
            .30+i*.075,.0025,10,100
        ),

        new THREE.MeshBasicMaterial({

            color:0x25ff96,

            transparent:true,

            opacity:.65-i*.075

        })
    );

    ring.rotation.x=Math.PI/2;
    ring.position.y=-.035;

    scene.add(ring);
}

const grid=new THREE.GridHelper(
    6,45,0x227c51,0x0a4026
);

grid.position.y=-.045;

scene.add(grid);


let model=null;

let bones={};

let rest=new Map();

let selectedJoint="knee";

let phase=0;

let playing=false;

let condition=DATA.conditions[0];

const opposite=DATA.conditions[
    DATA.conditions.length-1
];

const labels={
    pelvis:"Таз",

    hip:"Тазобедренный сустав",

    knee:"Коленный сустав",

    ankle:"Голеностопный сустав"

};

const scoreKeys={
    pelvis:"GVS_aSagP",

    hip:"GVS_aSagH",

    knee:"GVS_aSagK",

    ankle:"GVS_aSagA"

};

const colors={

    Baseline:"#56ffae",

    Verbal:"#5df5aa",

    VR:"#ffbf75"

};



function getBone(name){

    const normalize=x=>x.toLowerCase()
        .replace(/[^a-z0-9]/g,"");

    const aliases={

        LeftUpLeg:["thigh_l","LeftUpperLeg"],
        RightUpLeg:["thigh_r","RightUpperLeg"],

        LeftLeg:["calf_l","LeftLowerLeg"],
        RightLeg:["calf_r","RightLowerLeg"],

        LeftFoot:["foot_l","LeftFoot"],
        RightFoot:["foot_r","RightFoot"],

        LeftToeBase:["ball_l","LeftToes"],
        RightToeBase:["ball_r","RightToes"],

        LeftArm:["upperarm_l","LeftUpperArm"],
        RightArm:["upperarm_r","RightUpperArm"],

        LeftForeArm:["lowerarm_l","LeftLowerArm"],
        RightForeArm:["lowerarm_r","RightLowerArm"],

        LeftHand:["hand_l","LeftHand"],
        RightHand:["hand_r","RightHand"],

        Hips:["pelvis","Hips"]
    };

    const targets=[
        name,...(aliases[name]||[])
    ].map(normalize);

    const available=Object.values(bones);

    return available.find(
        b=>targets.includes(normalize(b.name))
    ) || available.find(
        b=>targets.includes(
            normalize(b.name).replace(/^mixamorig/,"")
        )
    );
}

let forward=new THREE.Vector3(0,0,1);

function detectForward(){

    const foot=getBone("LeftFoot");
    const toe=getBone("LeftToeBase");

    if(foot && toe){

        const direction=toe.getWorldPosition(
            new THREE.Vector3()
        ).sub(
            foot.getWorldPosition(
                new THREE.Vector3()
            )
        );

        direction.y=0;

        if(direction.length()>.001){
            forward.copy(direction.normalize());
        }
    }
}

function legDirection(a){

    return forward.clone()
        .multiplyScalar(Math.sin(a))
        .add(new THREE.Vector3(
            0,-Math.cos(a),0
        ));
}

function footDirection(a){

    return forward.clone()
        .multiplyScalar(Math.cos(a))
        .add(new THREE.Vector3(
            0,Math.sin(a),0
        ));
}

function aimBone(bone,child,direction){

    if(!bone || !child)return;

    model.updateMatrixWorld(true);

    const p=bone.getWorldPosition(
        new THREE.Vector3()
    );

    const q=child.getWorldPosition(
        new THREE.Vector3()
    );

    const old=q.sub(p).normalize();

    const rotation=new THREE.Quaternion()
        .setFromUnitVectors(
            old,direction.clone().normalize()
        );

    const world=bone.getWorldQuaternion(
        new THREE.Quaternion()
    );

    const parent=bone.parent.getWorldQuaternion(
        new THREE.Quaternion()
    );

    bone.quaternion.copy(
        parent.invert().multiply(
            rotation.multiply(world)
        )
    );

    model.updateMatrixWorld(true);
}


const markers={};

const clickable=[];

function createMarker(name){

    const group=new THREE.Group();

    const point=new THREE.Mesh(

        new THREE.SphereGeometry(.017,24,16),

        new THREE.MeshBasicMaterial({
            color:0x9fffd1
        })
    );

    point.userData.joint=name;

    clickable.push(point);

    group.add(point);


    const circle=new THREE.Mesh(

        new THREE.TorusGeometry(
            .043,.002,12,64
        ),

        new THREE.MeshBasicMaterial({
            color:0x25ff96
        })
    );

    group.add(circle);

    scene.add(group);

    markers[name]={group,point,circle};
}

["pelvis","hip","knee","ankle"].forEach(createMarker);


const loader=new GLTFLoader();

const raw=Uint8Array.from(
    atob(ASSET),c=>c.charCodeAt(0)
).buffer;


loader.parse(raw,"",gltf=>{

    model=gltf.scene;

    root.add(model);

    const meshes=[];

    model.traverse(obj=>{

        if(obj.isBone){

            bones[obj.name]=obj;

            rest.set(obj,obj.quaternion.clone());
        }

        if(obj.isMesh){

            meshes.push(obj);
        }
    });


    const box=new THREE.Box3().setFromObject(model);

    const size=box.getSize(new THREE.Vector3());

    const center=box.getCenter(new THREE.Vector3());

    const scale=1.82/size.y;

    root.scale.setScalar(scale);

    root.position.set(
        -center.x*scale,
        -box.min.y*scale,
        -center.z*scale
    );


    for(const mesh of meshes){

        mesh.material=bodyMaterial;

        mesh.frustumCulled=false;

        let wire;

        if(mesh.isSkinnedMesh){

            wire=new THREE.SkinnedMesh(
                mesh.geometry,
                wireMaterial
            );

            wire.bindMode=mesh.bindMode;

            wire.bind(
                mesh.skeleton,
                mesh.bindMatrix
            );

        }else{

            wire=new THREE.Mesh(
                mesh.geometry,
                wireMaterial
            );
        }

        wire.position.copy(mesh.position);

        wire.quaternion.copy(mesh.quaternion);

        wire.scale.copy(mesh.scale);

        wire.frustumCulled=false;

        mesh.parent.add(wire);
    }

    model.updateMatrixWorld(true);


    root.updateMatrixWorld(true);

    detectForward();

    const required=[
        "Hips",
        "LeftUpLeg","LeftLeg","LeftFoot",
        "LeftToeBase",
        "RightUpLeg","RightLeg","RightFoot",
        "RightToeBase"
    ];

    const missing=required.filter(
        name=>!getBone(name)
    );

    if(missing.length){

        $("loading").textContent=
            "Скелет модели несовместим: "+
            missing.join(", ");

        model=null;

        return;
    }

    camera.position.copy(
        forward.clone().multiplyScalar(3.9)
    );

    camera.position.y=1.1;
    orbit.update();

    // Natural A-pose for the reference view.
    

    for(const side of ["Left","Right"]){

        const upper=getBone(side+"Arm");

        const lower=getBone(side+"ForeArm");

        const hand=getBone(side+"Hand");

        const sign=side==="Left"?1:-1;

        aimBone(
            upper,lower,
            new THREE.Vector3(sign*.65,-.76,0)
        );

        aimBone(
            lower,hand,
            new THREE.Vector3(sign*.48,-.87,.08)
        );
    }

    rest.clear();

    model.traverse(obj=>{

        if(obj.isBone){

            rest.set(
                obj,obj.quaternion.clone()
            );
        }
    });

    $("loading").style.display="none";

    updatePose();

},error=>{

    $("loading").textContent=
        "Ошибка загрузки GLB: "+error.message;

});


// Research-driven leg pose

function angle(curve,p){

    const i=Math.floor(p);

    const j=Math.min(100,i+1);

    return curve[i]+(
        curve[j]-curve[i]
    )*(p-i);
}

function readAngles(){

    const curves=DATA.motion[condition];

    return {
        pelvis:angle(curves.pelvis,phase),
        hip:angle(curves.hip,phase),

        knee:angle(curves.knee,phase),

        ankle:angle(curves.ankle,phase)

    };
}



function updatePose(){

    if(!model)return;

    for(const [bone,q] of rest){
        bone.quaternion.copy(q);
    }

    model.updateMatrixWorld(true);

    const side=DATA.side==="RIGHT"
        ?"Right":"Left";

    const pelvis=getBone("Hips");
    const hip=getBone(side+"UpLeg");
    const knee=getBone(side+"Leg");
    const ankle=getBone(side+"Foot");
    const toe=getBone(side+"ToeBase");

    const a=readAngles();

    const p=THREE.MathUtils.degToRad(a.pelvis);
    const h=THREE.MathUtils.degToRad(a.hip);
    const k=THREE.MathUtils.degToRad(a.knee);
    const f=THREE.MathUtils.degToRad(a.ankle);

    // Illustrative sagittal-plane retargeting.
    // Not a clinically validated reconstruction.

    if(pelvis){

        const axis=new THREE.Vector3(0,1,0)
            .cross(forward).normalize();

        const rotation=new THREE.Quaternion()
            .setFromAxisAngle(axis,p);

        const world=pelvis.getWorldQuaternion(
            new THREE.Quaternion()
        );

        const parent=pelvis.parent.getWorldQuaternion(
            new THREE.Quaternion()
        );

        pelvis.quaternion.copy(
            parent.invert().multiply(
                rotation.multiply(world)
            )
        );

        model.updateMatrixWorld(true);
    }

    const thigh=h-p;
    const shank=thigh-k;

    aimBone(
        hip,knee,
        legDirection(thigh)
    );

    aimBone(
        knee,ankle,
        legDirection(shank)
    );

    aimBone(
        ankle,toe,
        footDirection(shank+f)
    );

    model.updateMatrixWorld(true);

    const selected={pelvis,hip,knee,ankle};

    for(const [name,bone] of Object.entries(selected)){

        if(!bone)continue;

        const marker=markers[name];

        marker.group.position.copy(
            bone.getWorldPosition(
                new THREE.Vector3()
            )
        );

        marker.circle.quaternion.copy(
            camera.quaternion
        );

        const active=name===selectedJoint;

        marker.circle.scale.setScalar(
            active?1.6:1
        );

        marker.circle.material.color.set(
            active?0xffcf84:0x58ffab
        );

        marker.point.material.color.set(
            active?0xffdf9e:0x9affcb
        );
    }
}

// Scientific dashboard

$("subject").textContent=DATA.subject;

$("side").textContent=
    DATA.side==="RIGHT"
    ?"Исследуемая нога: правая"
    :"Исследуемая нога: левая";


DATA.conditions.forEach(name=>{

    const option=document.createElement("option");

    option.value=name;

    option.textContent=name;

    $("condition").appendChild(option);
});


function drawGraph(){

    const canvas=$("graph");

    const ctx=canvas.getContext("2d");

    const w=canvas.clientWidth;

    const h=165;

    if(w<10)return;

    canvas.width=w;
    canvas.height=h;

    const arrays=DATA.conditions.map(
        name=>DATA.motion[name][selectedJoint]
    );

    const values=arrays.flat();

    const min=Math.min(...values)-5;

    const max=Math.max(...values)+5;

    const px=x=>38+x*(w-53)/100;

    const py=y=>12+(max-y)/(max-min)*(h-34);

    ctx.font="10px Arial";

    for(let i=0;i<5;i++){

        const y=12+i*(h-34)/4;

        ctx.strokeStyle="#175b3a";

        ctx.beginPath();

        ctx.moveTo(38,y);

        ctx.lineTo(w-15,y);

        ctx.stroke();

        ctx.fillStyle="#6ab993";

        ctx.fillText(
            (max-i*(max-min)/4).toFixed(0)+"°",
            3,y+3
        );
    }

    DATA.conditions.forEach(name=>{

        const array=DATA.motion[name][selectedJoint];

        ctx.strokeStyle=colors[name];

        ctx.lineWidth=name===condition?2.4:1.2;

        ctx.beginPath();

        array.forEach((value,i)=>{

            if(i===0){
                ctx.moveTo(px(i),py(value));
            }else{
                ctx.lineTo(px(i),py(value));
            }

        });

        ctx.stroke();

    });


    ctx.strokeStyle="#d9f9ff";

    ctx.lineWidth=1;

    ctx.beginPath();

    ctx.moveTo(px(phase),8);

    ctx.lineTo(px(phase),h-20);

    ctx.stroke();


    ctx.fillStyle="#8bd5b1";

    [0,25,50,75,100].forEach(i=>{

        ctx.fillText(
            i+"%",
            px(i)-9,h-4
        );
    });

}


function updateDashboard(){

    const a=readAngles();

    
    $("pelvisValue").textContent=
        a.pelvis.toFixed(1)+"°";

    $("hipValue").textContent=
        a.hip.toFixed(1)+"°";
    

    $("kneeValue").textContent=a.knee.toFixed(1)+"°";

    $("ankleValue").textContent=a.ankle.toFixed(1)+"°";

    $("phaseCircle").textContent=
        Math.round(phase)+"%";

    $("phaseText").textContent=
        "Цикл ходьбы: "+Math.round(phase)+"%";

    $("phase").value=phase;

    $("jointLabel").textContent=labels[selectedJoint];


    const scores=DATA.scores[condition]||{};

    $("gps").textContent=
        scores.GPS_a===undefined
        ?"—"
        :scores.GPS_a.toFixed(1)+"°";


    const gvs=scores[scoreKeys[selectedJoint]];

    $("gvs").textContent=
        gvs===undefined?"—":gvs.toFixed(1)+"°";


    const comparison=condition===opposite
        ?DATA.conditions[0]
        :opposite;

    const other=angle(
        DATA.motion[comparison][selectedJoint],
        phase
    );

    const difference=other-a[selectedJoint];

    $("difference").textContent=
        difference.toFixed(1)+"°";

    drawGraph();
}


$("legend").innerHTML=DATA.conditions.map(name=>
    `<span style="color:${colors[name]}">● ${name}</span>`
).join("");


function selectJoint(name){

    selectedJoint=name;

    document.querySelectorAll(".joint").forEach(b=>{

        b.classList.toggle(
            "active",
            b.dataset.joint===name
        );
    });

    updateDashboard();
}

document.querySelectorAll(".joint").forEach(b=>{

    b.onclick=()=>selectJoint(b.dataset.joint);

});


const raycaster=new THREE.Raycaster();

renderer.domElement.addEventListener(
    "click",event=>{

        const rect=
            renderer.domElement.getBoundingClientRect();

        const mouse=new THREE.Vector2(

            (event.clientX-rect.left)/rect.width*2-1,

            -(event.clientY-rect.top)/rect.height*2+1

        );

        raycaster.setFromCamera(mouse,camera);

        const hits=raycaster.intersectObjects(clickable);

        if(hits.length){

            selectJoint(
                hits[0].object.userData.joint
            );
        }
    }
);


$("play").onclick=()=>{

    playing=!playing;

    $("play").textContent=
        playing?"Ⅱ Пауза":"▶ Движение";
};


$("front").onclick=()=>{

    orbit.autoRotate=false;

    camera.position.set(0,1.1,3.9);

    orbit.update();
};


$("sideView").onclick=()=>{

    orbit.autoRotate=false;

    camera.position.set(3.9,1.1,0);

    orbit.update();
};


$("rotate").onclick=()=>{

    orbit.autoRotate=!orbit.autoRotate;

    orbit.autoRotateSpeed=1.5;
};


$("condition").onchange=e=>{

    condition=e.target.value;

    updatePose();

    updateDashboard();
};


$("phase").oninput=e=>{

    playing=false;

    $("play").textContent="▶ Движение";

    phase=Number(e.target.value);

    updatePose();

    updateDashboard();
};


new ResizeObserver(()=>{

    const w=stage.clientWidth;

    const h=stage.clientHeight;

    if(!w||!h)return;

    camera.aspect=w/h;

    camera.updateProjectionMatrix();

    renderer.setSize(w,h);

    composer.setSize(w,h);

}).observe(stage);




// ====================================
// NEUROVOICE
// ====================================

function speak(text){

    $("voiceStatus").textContent=text;

    if(!("speechSynthesis" in window)){
        return;
    }

    speechSynthesis.cancel();

    const message=
        new SpeechSynthesisUtterance(text);

    message.lang="ru-RU";
    message.rate=.95;
    message.pitch=.9;

    const voices=speechSynthesis.getVoices();

    const russian=voices.find(
        v=>v.lang.startsWith("ru")
    );

    if(russian){
        message.voice=russian;
    }

    speechSynthesis.speak(message);
}

function report(){

    const angles=readAngles();

    const value=angles[selectedJoint];

    const scores=DATA.scores[condition]||{};

    const name=labels[selectedJoint];

    let text=
        name+". Текущий угол "+
        value.toFixed(1).replace(".",",")+
        " градуса. Фаза цикла ходьбы "+
        Math.round(phase)+" процентов.";

    if(Number.isFinite(scores.GPS_a)){

        text+=" Показатель GPS: "+
            scores.GPS_a.toFixed(1)
            .replace(".",",")+" градуса.";
    }

    text+=" Эти данные описывают движение, "+
        "а не тяжесть заболевания.";

    speak(text);
}

function voiceCommand(input){

    const q=input.toLowerCase().trim();

    if(/тяжест|диагноз|лечен|лекарств/.test(q)){

        speak(
            "Я могу объяснять исследовательские "+
            "показатели. Диагноз и функциональный "+
            "уровень определяет специалист."
        );

        return;
    }

    if(/пауза|останови|стоп/.test(q)){

        playing=false;

        $("play").textContent="▶ Движение";

        speak("Анимация остановлена.");

        return;
    }

    if(/включи|запусти|движение/.test(q)){

        playing=true;

        $("play").textContent="Ⅱ Пауза";

        speak("Воспроизвожу цикл ходьбы.");

        return;
    }

    if(/сбоку/.test(q)){

        $("sideView").click();

        speak("Вид сбоку.");

        return;
    }

    if(/спереди/.test(q)){

        $("front").click();

        speak("Вид спереди.");

        return;
    }

    if(/gps|джипиэс|джи пи эс/.test(q)){

        const score=
            (DATA.scores[condition]||{}).GPS_a;

        let text=
            "GPS показывает суммарное отклонение "+
            "измеренного профиля походки "+
            "от эталонного профиля.";

        if(Number.isFinite(score)){
            text+=" Значение: "+
                score.toFixed(1).replace(".",",")+
                " градуса.";
        }

        speak(text);

        return;
    }

    if(/gvs|дживиэс|джи ви эс/.test(q)){

        const score=(DATA.scores[condition]||{})[
            scoreKeys[selectedJoint]
        ];

        let text=
            "GVS описывает отклонение "+
            "выбранной суставной кривой "+
            "от эталонной.";

        if(Number.isFinite(score)){
            text+=" Значение: "+
                score.toFixed(1).replace(".",",")+
                " градуса.";
        }

        speak(text);

        return;
    }

    if(/голеностоп|стопа|стопу/.test(q)){
        selectJoint("ankle");
    }
    else if(/колен/.test(q)){
        selectJoint("knee");
    }
    else if(/тазобедрен|бедро/.test(q)){
        selectJoint("hip");
    }
    else if(/таз/.test(q)){
        selectJoint("pelvis");
    }
    else if(/baseline|базов/.test(q)){
        condition="Baseline";
    }
    else if(/verbal|голосов.*подсказ/.test(q)){
        condition="Verbal";
    }
    else if(/виртуальн|vr|ви ар/.test(q)){
        condition="VR";
    }
    else if(!/показател|результат|объясни/.test(q)){

        speak(
            "Выберите сустав, условие исследования "+
            "или попросите объяснить GPS и GVS."
        );

        return;
    }

    if(!DATA.motion[condition]){
        condition=DATA.conditions[0];
    }

    $("condition").value=condition;

    updatePose();
    updateDashboard();

    report();
}

$("speakData").onclick=report;

$("stopVoice").onclick=()=>{

    if("speechSynthesis" in window){
        speechSynthesis.cancel();
    }
};

$("sendVoice").onclick=()=>{
    voiceCommand($("voiceText").value);
};

$("voiceText").addEventListener(
    "keydown",e=>{

        if(e.key==="Enter"){
            voiceCommand(e.target.value);
        }
    }
);

$("listen").onclick=()=>{

    const SpeechRecognition=
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if(!SpeechRecognition){

        $("voiceStatus").textContent=
            "Микрофон не поддерживается браузером. "+
            "Введите команду текстом.";

        return;
    }

    const recognition=new SpeechRecognition();

    recognition.lang="ru-RU";

    recognition.interimResults=false;

    recognition.continuous=false;

    recognition.onresult=e=>{

        const text=e.results[0][0].transcript;

        $("voiceText").value=text;

        voiceCommand(text);
    };

    recognition.onerror=()=>{

        $("voiceStatus").textContent=
            "Распознавание недоступно. "+
            "Используйте текстовую команду.";
    };

    recognition.onstart=()=>{

        $("voiceStatus").textContent=
            "Слушаю команду...";
    };

    try{
        recognition.start();
    }
    catch(e){

        $("voiceStatus").textContent=
            "Разрешите микрофон "+
            "или введите команду текстом.";
    }
};


let previous=performance.now();

let lastUpdate=0;

function animate(now){

    requestAnimationFrame(animate);

    const dt=Math.min(
        (now-previous)/1000,.05
    );

    previous=now;

    if(playing){

        phase=(
            phase+dt*40*Number($("speed").value)
        )%100;
    }

    orbit.update();

    updatePose();

    if(now-lastUpdate>90){

        updateDashboard();

        lastUpdate=now;
    }

    composer.render();
}

requestAnimationFrame(animate);

</script>
</body>
</html>
"""


def show_gait_3d(*args, **kwargs):

    st.subheader("NeuroMotion — лаборатория движения")

    model = read_model()
    if not model:
        st.error("Не найден файл assets/neuro_male.glb")
        return

    if not model.startswith(b"glTF"):
        st.error("Файл 3D-модели повреждён.")
        return

    motion, scores = load_data()

    if not motion:
        st.warning("Для 3D-анализа нужны исследовательские CSV в data/research.")
        return

    participants = set.intersection(*[
        set(zip(df["subject"], df["side"]))
        for df in motion.values()
    ])

    if not participants:
        st.warning("Нет общих участников исследования.")
        return

    subject, side = st.selectbox(

        "Выберите участника исследования",

        sorted(participants),

        format_func=lambda x:
            x[0] + " · " +
            ("Правая нога" if x[1] == "RIGHT"
             else "Левая нога"),

        key="neuro_hud_participant"

    )

    curves = {}

    values = {}

    for condition, df in motion.items():

        result = get_curves(df, subject, side)

        if result is None:
            continue

        curves[condition] = result

        values[condition] = get_scores(
            scores.get(condition),
            subject,
            side
        )

    if not curves:

        st.warning("Нет полных измерений.")

        return

    payload = {

        "subject": subject,

        "side": side,

        "conditions": list(curves),

        "motion": curves,

        "scores": values

    }

    model64 = base64.b64encode(
        model
    ).decode("ascii")

    html = HTML.replace(
        "__PAYLOAD__",
        json.dumps(payload, allow_nan=False)
    ).replace(
        "__MODEL_BASE64__",
        model64
    )

    components.html(
        html,
        height=1500,
        scrolling=True
    )

    st.caption(
        "De Mulder et al., KU Leuven, 2024. "
        "DOI: 10.48804/JUNNWW. "
        "Геометрия: Quaternius Superhero Male, CC0."
    )

    with st.expander("Научные показатели"):

        table = pd.DataFrame(values).T

        table = table.rename(columns={

            "GPS_a": "GPS, °",

            "GVS_aSagP": "GVS — таз, °",

            "GVS_aSagH": "GVS — бедро, °",

            "GVS_aSagK": "GVS — колено, °",

            "GVS_aSagA": "GVS — голеностоп, °"

        })

        st.dataframe(
            table,
            width="stretch"
        )

        st.write(
            "GPS и GVS взяты непосредственно "
            "из исследовательских таблиц. "
            "Они характеризуют отклонения походки, "
            "но не определяют уровень GMFCS автоматически."
        )

    st.info(
        "Движение исследуемой ноги визуализируется "
        "по измеренным суставным углам. "
        "Форма тела, положение рук и второй ноги условны. "
        "Углы таза и исследуемой ноги взяты из CSV. "
        "Пространственная реконструкция требует "
        "дополнительной биомеханической валидации."
    )

