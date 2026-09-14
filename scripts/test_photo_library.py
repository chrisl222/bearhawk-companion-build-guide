"""Focused regression checks for provenance, review gating and site links."""
import unittest,json,uuid,hashlib,shutil
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from urllib.parse import urlsplit,unquote
from PIL import Image
import import_photos as imp
import photo_library as lib
from validate_batch import PageLinks

class PhotoLibraryTests(unittest.TestCase):
    def setUp(self):
        work=lib.ROOT/'work';work.mkdir(exist_ok=True)
        self.root=(work/('photo-test-'+uuid.uuid4().hex)).resolve();assert self.root.is_relative_to(work.resolve())
        self.root.mkdir()
        self.addCleanup(shutil.rmtree,self.root)
    def test_curated_metadata(self):
        self.assertEqual(lib.validate(),len(lib.public_photos()))
        self.assertGreater(len(lib.public_photos()),0)
        for p in lib.public_photos():lib.validate_metadata(p)
    def test_missing_review_and_invalid_model_rejected(self):
        p=lib.public_photos()[0].copy();p['reviewStatus']='approved'
        with self.assertRaises(ValueError):lib.validate_metadata(p)
        p['humanReviewer']='Fixture reviewer';p['aircraftModel']='Guessed Companion'
        with self.assertRaises(ValueError):lib.validate_metadata(p)
    def test_path_escape_rejected(self):
        with self.assertRaises(ValueError):imp.contained(self.root,'../outside.jpg')
    def test_directory_preserves_html_captions_paths_and_duplicates(self):
        source=self.root/'cd';(source/'wing/images').mkdir(parents=True)
        Image.new('RGB',(100,120),'gray').save(source/'wing/images/original.jpg')
        (source/'duplicate.jpg').write_bytes((source/'wing/images/original.jpg').read_bytes())
        html='<html><p>Original context</p><img src="images/original.jpg" alt="Original caption"><img src="../../outside.jpg"></html>'
        (source/'wing/index.html').write_text(html)
        out=self.root/'batch';args=SimpleNamespace(source=source,out=out,source_name='CD fixture',source_type='Builder Manual',source_url='',builder='')
        imp.directory(args);records=json.loads((out/'manifest.json').read_text())
        r=next(r for r in records if r['originalPath']=='wing/images/original.jpg')
        self.assertEqual(r['originalCaption'],'Original caption');self.assertEqual(r['reviewStatus'],'pending')
        self.assertEqual((out/'originals/wing/index.html').read_text(),html)
        self.assertEqual(sum('duplicateOf' in r for r in records),1)
        self.assertEqual(r['aircraftModel'],'Unknown')
    def test_publish_pending_and_missing_rights(self):
        data=self.root/'specs';data.mkdir();(data/'photos.json').write_text('[]')
        (data/'taxonomy.json').write_bytes((lib.DATA/'taxonomy.json').read_bytes())
        batch=self.root/'batch';batch.mkdir();(batch/'manifest.json').write_text('[{"reviewStatus":"pending"}]')
        with patch.object(imp,'DATA',data),patch.object(imp,'ROOT',self.root):
            imp.publish(SimpleNamespace(batch=batch));self.assertEqual(json.loads((data/'photos.json').read_text()),[])
            p=lib.public_photos()[0].copy();p.update(reviewStatus='approved',humanReviewer='Fixture reviewer',rightsBasis='')
            (batch/'manifest.json').write_text(json.dumps([p]))
            with self.assertRaises(ValueError):imp.publish(SimpleNamespace(batch=batch))
            self.assertFalse((self.root/'docs').exists())
    def test_approved_roundtrip(self):
        data=self.root/'specs';data.mkdir();(data/'photos.json').write_text('[]')
        (data/'taxonomy.json').write_bytes((lib.DATA/'taxonomy.json').read_bytes())
        batch=self.root/'batch';(batch/'originals').mkdir(parents=True)
        p=lib.public_photos()[0].copy();p.update(id='fixture-photo',reviewStatus='approved',humanReviewer='Fixture reviewer',stagedPath='originals/example.png',originalFilename='example.png',originalPath='example.png')
        file=batch/p['stagedPath'];Image.new('RGB',(120,130),'blue').save(file);p['sha256']=hashlib.sha256(file.read_bytes()).hexdigest()
        (batch/'manifest.json').write_text(json.dumps([p]))
        with patch.object(imp,'DATA',data),patch.object(imp,'ROOT',self.root):imp.publish(SimpleNamespace(batch=batch))
        out=json.loads((data/'photos.json').read_text());self.assertEqual(len(out),1);lib.validate_metadata(out[0])
        self.assertEqual((self.root/'docs'/out[0]['originalImage']).read_bytes(),file.read_bytes())
    def test_site_links_and_old_bookmarks(self):
        docs=(lib.ROOT/'docs').resolve();pages={}
        for f in docs.rglob('*.html'):
            p=PageLinks();p.feed(f.read_text(encoding='utf-8'));pages[f]=p
        checked=0
        for f,p in pages.items():
            for href in p.links:
                url=urlsplit(href)
                if url.scheme or url.netloc:continue
                dest=(f.parent/unquote(url.path)).resolve() if url.path else f
                if dest.is_dir():dest=dest/'index.html'
                self.assertTrue(dest.is_relative_to(docs),(f,href));self.assertTrue(dest.exists(),(f,href))
                if url.fragment and dest in pages:self.assertIn(unquote(url.fragment),pages[dest].ids,(f,href))
                checked+=1
        old=lib.read_legacy()
        for ref in old:
            self.assertIn(ref['id'],pages[docs/'photos/index.html'].ids)
            self.assertIn(ref['id'],pages[docs/'photos/reference-index/index.html'].ids)
        print('SITE_LINKS',len(pages),'pages',checked,'local links;',len(old),'old bookmarks preserved')
    def test_build_artifacts_unchanged(self):
        file=lib.ROOT/'work/photo-library/baseline.json'
        if not file.exists():self.skipTest('Session baseline not present')
        for name,h in json.loads(file.read_text()).items():self.assertEqual(hashlib.sha256((lib.ROOT/name).read_bytes()).hexdigest(),h,name)

if __name__=='__main__':unittest.main()
