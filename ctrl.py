import logging
import subprocess

import db
import ui
import config

class Controller:
  def __init__(self, args):
    self.log = logging.getLogger('root')
    self.args = args
    self.cfg = config.Config(self.args.config_file)

    self.dbase = db.Db(self.args.dir_list, self.args.file_pattern_list)
    self.dbase.build()

    self.view = ui.NavUi(self.cfg)

    self.view.add_image_open_click_handler(
      self._on_image_open_click_handler)
    pass

  def main(self):
    self._show_all_views()
    self.view.main()
    pass

  def _show_all_views(self):
    self.view.clear_images()
    for viewname in self.dbase.get_view_names():
      self.view.add_folder(
        viewname, viewname, self._on_folder_click_handler)
      pass
    pass

  def _add_image_item(self, item):
    self.view.add_image(
      item.get_id(),
      item.get_full_path(),
      item.get_display_name())
    pass        

  def _on_folder_click_handler(self, identifier, name):
    self.log.debug('Folder %s clicked (id=%s)', name, identifier)
    items = self.dbase.get_view_item_identifiers(identifier)
    if items is not None:
      self.view.clear_images()
      for item_id in items:
        item = self.dbase.get_item_from_id(item_id)
        self._add_image_item(item)
        pass
      pass
    pass

  def _on_image_open_click_handler(self, identifier, name):
    item = self.dbase.get_item_from_id(identifier)
    if None is not item:
      path = item.get_full_path()
      cmd = [self.cfg.get_option('open_image_cmd'), path]
      self.log.info('Opening image %s (id=%s, path=%s) with command=%s',
        name, identifier, path, str(cmd))
      subprocess.call(cmd)
      pass
    else:
      self.log.warning('Image %s clicked but id=%s not found in db',
        name, identifier)
      pass
    pass

    
