<template>
  <tr>
    <td>{{ fileInfo.filepath }}</td>
    <td>{{ fileInfo.count }}</td>
    <td><button class="button">Actions here</button></td>
  </tr>
</template>

<script>
export default {
  name: 'bulk-view-table-row',
  props: [ 'fileInfo' ]
}
</script>

<style>
</style>
