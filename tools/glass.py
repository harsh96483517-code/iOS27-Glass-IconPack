#!/usr/bin/env python3
"""Ek ek icon ko upscale karke iOS-27 glass effect lagata hai.
Usage: python tools/glass.py --input input --output out --size 4096 [--sr]
Resume-safe: jo output pehle se bana hai use skip karta hai."""
import argparse, os, sys, glob, time, urllib.request
import numpy as np, cv2
from PIL import Image

SR_URL = "https://github.com/Saafke/FSRCNN_Tensorflow/raw/master/models/FSRCNN_x4.pb"

def load_sr(path):
    try:
        if not os.path.exists(path):
            urllib.request.urlretrieve(SR_URL, path)
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        sr.readModel(path); sr.setModel("fsrcnn", 4)
        return sr
    except Exception as e:
        print("  [sr unavailable, Lanczos use hoga]", e); return None

def build_masks(S):
    f32 = np.float32
    yy, xx = np.mgrid[0:S, 0:S].astype(f32)
    x = ((xx + f32(.5)) / f32(S) * f32(2) - f32(1))
    y = ((yy + f32(.5)) / f32(S) * f32(2) - f32(1))
    del yy, xx
    n = f32(5.0)
    f = (np.abs(x) ** n + np.abs(y) ** n) ** (f32(1) / n)
    alpha = np.clip((f32(1) - f) * f32(S) / f32(2) / f32(1.6) + f32(.5), 0, 1)
    rim = np.clip((f - f32(.93)) / f32(.07), 0, 1) * alpha
    rim_in = np.clip((f - f32(.975)) / f32(.025), 0, 1) * alpha
    ang = np.arctan2(y, x).astype(f32)
    d = lambda deg: f32(np.deg2rad(deg))
    light = (np.clip(np.cos(ang - d(-135)), 0, 1) ** f32(2)
             + np.clip(np.cos(ang - d(45)), 0, 1) ** f32(3) * f32(.55))
    gl = np.clip(f32(1) - ((y + f32(.62)) / f32(.75)) ** f32(2)
                 - (x / f32(1.05)) ** f32(2) * f32(.35), 0, 1)
    gloss = gl ** f32(1.2) * np.clip(f32(1) - (y + f32(1)) / f32(1.1), 0, 1) * f32(.30)
    del gl
    sheen = np.clip(f32(1) - np.abs((x + y * f32(.9)) + f32(.15)) / f32(.22), 0, 1) ** f32(2) * f32(.07)
    bot = np.clip((y - f32(.55)) / f32(.45), 0, 1) * f32(.10)
    del x, y
    return dict(f=f, alpha=alpha, rim=rim, rim_in=rim_in, ang=ang,
                light=light, L=(gloss + sheen + bot)[..., None])


def glass(rgb, M, S):
    a = rgb.astype(np.float32) / np.float32(255)
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV); hsv[..., 1] = np.clip(hsv[..., 1] * np.float32(1.10), 0, 1)
    a = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    blur = cv2.GaussianBlur(a, (0, 0), S * .03)
    w = (np.clip((M["f"] - np.float32(.88)) / np.float32(.12), 0, 1) ** np.float32(1.5) * np.float32(.35))[..., None]
    a = a * (np.float32(1) - w) + np.clip(blur * np.float32(1.08) + np.float32(.02), 0, 1) * w
    sh = (M["rim"] ** np.float32(1.2) * np.clip(np.cos(M["ang"] - np.float32(np.deg2rad(45))), 0, 1) * np.float32(.10))[..., None]
    a = a * (np.float32(1) - sh)
    a = a + (np.float32(1) - a) * M["L"]
    r = (M["rim"] ** np.float32(1.6) * M["light"] * np.float32(.55) + M["rim_in"] * np.float32(.35) * (np.float32(.4) + M["light"] * np.float32(.6)))[..., None]
    a = a + (np.float32(1) - a) * np.clip(r, 0, 1)
    hl = (np.clip((M["f"] - np.float32(.992)) / np.float32(.008), 0, 1) * M["alpha"] * np.float32(.12))[..., None]
    a = a * (np.float32(1) - hl)
    out = np.dstack([np.clip(a, 0, 1), M["alpha"]])
    return Image.fromarray((out * 255 + .5).astype(np.uint8), "RGBA")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="input"); ap.add_argument("--output", default="out")
    ap.add_argument("--size", type=int, default=4096)
    ap.add_argument("--sr", action="store_true", help="AI upscaler (FSRCNN x4) try karo")
    a = ap.parse_args()
    os.makedirs(a.output, exist_ok=True)
    files = sorted(glob.glob(os.path.join(a.input, "*.png")))
    sr = load_sr("FSRCNN_x4.pb") if a.sr else None
    M = build_masks(a.size)
    for i, p in enumerate(files, 1):
        name = os.path.basename(p); dst = os.path.join(a.output, name)
        if os.path.exists(dst):
            print(f"[{i}/{len(files)}] {name} skip"); continue
        t = time.time()
        img = cv2.imread(p, cv2.IMREAD_COLOR)
        if sr is not None:
            try: img = sr.upsample(img)
            except Exception as e: print("  sr fail:", e)
        img = cv2.resize(img, (a.size, a.size), interpolation=cv2.INTER_LANCZOS4)
        blur = cv2.GaussianBlur(img, (0, 0), a.size / 700)
        img = cv2.addWeighted(img, 1.35, blur, -.35, 0)   # halka sharpen
        out = glass(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), M, a.size)
        out.save(dst)
        print(f"[{i}/{len(files)}] {name} done {time.time()-t:.1f}s", flush=True)

if __name__ == "__main__":
    main()
