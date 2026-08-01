import { useEffect, useRef } from 'react'
import * as THREE from 'three'
import { usePrefs } from '../hooks/usePrefs'

/** Lightweight WebGL starfield — drama motion only; calm falls back to null. */
export function Starfield3D() {
  const mountRef = useRef<HTMLDivElement>(null)
  const { motion, theme } = usePrefs()

  useEffect(() => {
    if (motion === 'calm') return
    const mount = mountRef.current
    if (!mount) return

    const w = mount.clientWidth || window.innerWidth
    const h = mount.clientHeight || window.innerHeight

    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(55, w / h, 0.1, 100)
    camera.position.z = 6

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    renderer.setSize(w, h)
    renderer.setClearColor(0x000000, 0)
    mount.appendChild(renderer.domElement)

    const count = 900
    const positions = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 18
      positions[i * 3 + 1] = (Math.random() - 0.5) * 12
      positions[i * 3 + 2] = (Math.random() - 0.5) * 10
    }
    const geo = new THREE.BufferGeometry()
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    const mat = new THREE.PointsMaterial({
      color: theme === 'ratri' ? 0xd2e2e6 : 0x3db5ad,
      size: 0.035,
      transparent: true,
      opacity: theme === 'ratri' ? 0.85 : 0.55,
      depthWrite: false,
    })
    const stars = new THREE.Points(geo, mat)
    scene.add(stars)

    // slow brass wire diamond
    const diamond = new THREE.Mesh(
      new THREE.OctahedronGeometry(0.55, 0),
      new THREE.MeshBasicMaterial({
        color: 0xa67c3d,
        wireframe: true,
        transparent: true,
        opacity: 0.45,
      }),
    )
    diamond.position.set(2.2, -0.4, 0)
    scene.add(diamond)

    let raf = 0
    let alive = true
    const tick = () => {
      if (!alive) return
      stars.rotation.y += 0.00055
      stars.rotation.x += 0.00015
      diamond.rotation.y += 0.008
      diamond.rotation.x += 0.003
      renderer.render(scene, camera)
      raf = requestAnimationFrame(tick)
    }
    tick()

    const onResize = () => {
      const nw = mount.clientWidth || window.innerWidth
      const nh = mount.clientHeight || window.innerHeight
      camera.aspect = nw / nh
      camera.updateProjectionMatrix()
      renderer.setSize(nw, nh)
    }
    window.addEventListener('resize', onResize)

    return () => {
      alive = false
      cancelAnimationFrame(raf)
      window.removeEventListener('resize', onResize)
      geo.dispose()
      mat.dispose()
      diamond.geometry.dispose()
      ;(diamond.material as THREE.Material).dispose()
      renderer.dispose()
      if (renderer.domElement.parentNode === mount) mount.removeChild(renderer.domElement)
    }
  }, [motion, theme])

  if (motion === 'calm') return null
  return <div ref={mountRef} className="starfield-3d" aria-hidden />
}
